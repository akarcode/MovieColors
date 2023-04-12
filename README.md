# Movie Colors

![movie_colors](https://user-images.githubusercontent.com/59408512/231383382-fbba68c2-7970-4a30-911c-12df5b1d4710.png)

This Python script can collect color values per packet via FFprobe and write them back into an image. The top of the image represents the highlights of an image and the bottom the shadows.

### Additional notes

- Be cautious with the escape characters in the file paths.
- This script does not write frames to your Harddisk as other similar script for this do.
- On a fast SSD drive it will take about 6min for the script to finish a 90min movie. The speed is limited to FFprobe, the additional math only takes about 1 second to complete.


### Requirements

**FFprobe** is used to read out the information from your movie.\
And you'll need to import **NumPy** and **PIL** in python.


### Changelog

v1.0 (Initial release)
