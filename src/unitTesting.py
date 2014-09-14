#!/usr/bin/python
from classes.UnitTesting import *

# Load the class
unitTesting = UnitTesting()

# Asserts the FeaturesExtractor class:
unitTesting.assertFeatureExtractor()
unitTesting.getResults()

# Asserts the Utils class:
unitTesting.assertUtils()
unitTesting.getResults()

# Asserts the BPNHandler class:
unitTesting.assertBPNHandler()
unitTesting.getResults()

# Get the final results
unitTesting.getFinalResults()