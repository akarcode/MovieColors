from PIL import Image, ImageFilter
import numpy as np
import subprocess

ffprobe = 'C:\\Program Files\\FFmpeg\\bin\\ffprobe.exe'
movie = 'C\\\\:/Folder/Movie.mkv'
output = 'C:\\Folder\\movie_colors.png'
starttime = '00\\:00\\:00'
endtime = '00\\:01\\:00'
croptop = '0'
cropbottom = '0'
nth = 10
height = 800
blur = 1

# ###########

grab_y = 'frame_tags=lavfi.signalstats.YLOW,lavfi.signalstats.YAVG,lavfi.signalstats.YHIGH,'
grab_u = 'lavfi.signalstats.ULOW,lavfi.signalstats.UAVG,lavfi.signalstats.UHIGH,'
grab_v = 'lavfi.signalstats.VLOW,lavfi.signalstats.VAVG,lavfi.signalstats.VHIGH'

ffprobe_args = (ffprobe, '-hide_banner', '-loglevel', 'error', '-select_streams', 'v:0',
                '-print_format', 'default=nokey=1:noprint_wrappers=1', '-f', 'lavfi',
                ('movie=' + movie + ',trim=\'' + starttime + '\':\'' + endtime + '\'' +
                ',crop=h=in_h-(' + croptop + '+' + cropbottom + '):y=' + croptop + ',signalstats'),
                '-show_entries', grab_y + grab_u + grab_v)

yuvdata = (subprocess.run(ffprobe_args, stdout=subprocess.PIPE, universal_newlines=True)).stdout.splitlines()


def convert_yuv_to_rgb(y, u, v):
    y = float(y) - 16
    u = float(u) - 128
    v = float(v) - 128
    r = max(0, (round(1.164 * y + 1.596 * v)))
    g = max(0, (round(1.164 * y - 0.392 * u - 0.813 * v)))
    b = max(0, (round(1.164 * y + 2.017 * u)))
    return [r, g, b]


colors, lowlights, highlights, lowlum, highlum = [], [], [], [], []

for i in range(0, len(yuvdata), 9 * nth):

    lowlights += convert_yuv_to_rgb(yuvdata[i], yuvdata[i + 3], yuvdata[i + 6])
    colors += convert_yuv_to_rgb(yuvdata[i + 1], yuvdata[i + 4], yuvdata[i + 7])
    highlights += convert_yuv_to_rgb(yuvdata[i + 2], yuvdata[i + 5], yuvdata[i + 8])

    lowlum += [255 - int(yuvdata[i])]
    highlum += [int(yuvdata[i + 2])]


gradient_height = int(len(yuvdata) / 9)
gradient_width = int(height / 2)

lowgradient = np.zeros((gradient_height, gradient_width, 4), np.uint8)
highgradient = np.zeros((gradient_height, gradient_width, 4), np.uint8)

for i in range(0, int(len(lowlights) / 3)):

    lowgradient[i, :, 0] = np.array(lowlights[i * 3 + 0]).astype(np.uint8)
    lowgradient[i, :, 1] = np.array(lowlights[i * 3 + 1]).astype(np.uint8)
    lowgradient[i, :, 2] = np.array(lowlights[i * 3 + 2]).astype(np.uint8)
    highgradient[i, :, 0] = np.array(highlights[i * 3 + 0]).astype(np.uint8)
    highgradient[i, :, 1] = np.array(highlights[i * 3 + 1]).astype(np.uint8)
    highgradient[i, :, 2] = np.array(highlights[i * 3 + 2]).astype(np.uint8)


for i in range(0, len(lowlum)):

    lowgradient[i, :, 3] = np.linspace(lowlum[i], 0, gradient_width, dtype=np.uint8)
    highgradient[i, :, 3] = np.linspace(highlum[i], 0, gradient_width, dtype=np.uint8)


lowimage = Image.fromarray(lowgradient, mode='RGBA').transpose(method=Image.Transpose.ROTATE_90)
highimage = Image.fromarray(highgradient, mode='RGBA').transpose(method=Image.Transpose.TRANSPOSE)

colors = bytes(colors)
width = int(len(colors) / 3)
img = Image.frombytes('RGB', (width, 1), colors)
img = img.resize((width, height))

img.paste(lowimage, (0, int(height / 2)), lowimage)
img.paste(highimage, (0, 0), highimage)
imgblur = img.filter(ImageFilter.BoxBlur(blur))

imgblur.save(output)
