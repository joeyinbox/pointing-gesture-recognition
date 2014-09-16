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
- Open a terminal and execute the `main.py` file (CLI-only version: `live.py`).
- Stand up and point!

![Live GUI](http://joeyclouvel.com/brookes/live-gui.png)

## Performances and Accuracy ##
The average pointed direction is **6.5 cm** off the target.

![Impacts heatmap](http://joeyclouvel.com/brookes/impacts-heatmap.png)

The current neural network features the following success percentages:
- **98.50 %** on training
- **88.10 %** on testing
- **88.10 %** on validation
- **70.83 %** on random data

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
- Get the average pointed direction accuracy.
- Get a graphic of all trajectories or all impacts relative to the target thanks to [matplotlib](http://matplotlib.org) as illustrated in the performance section.

## About ##
This experimentation is part of my Software Engineering Master's dissertation for [Oxford Brookes University](http://brookes.ac.uk) and is meant to be used on their [RoboThespian](https://www.engineeredarts.co.uk) unit.