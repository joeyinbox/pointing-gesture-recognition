# Pointing gesture recognition #

Automatic Recognition of Pointing Gestures.

## Requirements ##
- [Python](https://www.python.org) 2.7 or higher
- [PyOpenNI](https://github.com/jmendeth/PyOpenNI)
- [OpenCV](http://opencv.org) 2.4.9
- Depth sensor (Kinect, Asus Xtion Live)

## Getting started ##
- Open a terminal and execute the `body.py` file.
- Stand up and point!

## Configuration ##
- Auto-calibration needs to be enabled in the OpenNI file `FeatureExtraction.ini` by uncommenting and setting to 1 the line `UseAutoCalibration=1` under the **[LBS]** section.