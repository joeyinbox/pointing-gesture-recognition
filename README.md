# Pointing gesture recognition #

Automatic Recognition of Pointing Gestures in Python using a depth sensor.

## Requirements ##
- [Python](https://www.python.org) 2.7 or higher
- [PyOpenNI](https://github.com/jmendeth/PyOpenNI)
- [OpenCV](http://opencv.org) 2.4.9
- [NumPy](http://www.numpy.org) 1.8.x
- [PyQt](http://www.riverbankcomputing.co.uk/software/pyqt/download5) 5.3 (which requires [SIP](http://www.riverbankcomputing.co.uk/software/sip/download) 4.16 and [Qt](http://qt-project.org/downloads) 5.3)
- Depth sensor (e.g. Kinect, Asus Xtion Live)

## Getting started ##
- Open a terminal and execute the `main.py` file.
- Stand up and point!

## Configuration ##
- Auto-calibration needs to be enabled in the OpenNI file `FeatureExtraction.ini` by uncommenting and setting to 1 the line `UseAutoCalibration=1` under the **[LBS]** section.

## Advanced ##

### Record new dataset items ###
- Open a terminal and execute the `capture.py` file.
- Fill the GUI form and shoot!

### Train the network ###
- Open a terminal and execute the `training.py` file.
- You can choose what kind of data you will input alongside the network's parameters.

### Validate the network ###
- Open a terminal and execute the `validating.py` file.
- Same choice than the training part herein.

### Check accuracy ###
- Open a terminal and execute the `accuracy.py` file.
- More options coming.

## About ##
This experimentation is part of my Software Engineering Master's dissertation for [Oxford Brookes University](http://brookes.ac.uk) and is meant to be used on their [RoboThespian](https://www.engineeredarts.co.uk) unit.