# Pointing gesture recognition #

Automatic Recognition of Pointing Gestures.

## Requirements ##
- [Python](https://www.python.org) 2.7 or higher
- [PyOpenNI](https://github.com/jmendeth/PyOpenNI)
- [OpenCV](http://opencv.org) 2.4.9
- [PySDL2](https://bitbucket.org/marcusva/py-sdl2) 0.9.2 (which requires [PyPy](http://www.pypy.org) 1.8.0+)
- Depth sensor (e.g. Kinect, Asus Xtion Live)

## Getting started ##
- Open a terminal and execute the `main.py` file.
- Stand up and point!

## Configuration ##
- Auto-calibration needs to be enabled in the OpenNI file `FeatureExtraction.ini` by uncommenting and setting to 1 the line `UseAutoCalibration=1` under the **[LBS]** section.

## About ##
This experimentation is part of my Software Engineering Master's dissertation for [Oxford Brookes University](http://brookes.ac.uk) and is meant to be used on their [RoboThespian](https://www.engineeredarts.co.uk) unit.