#!/usr/bin/env python3
"""
Script to run all tests for the sentiment analysis API.
"""

import os
import sys
import unittest

# Add the project root directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

if __name__ == '__main__':
    # Discover and run all tests in the app/tests directory
    test_loader = unittest.TestLoader()
    test_suite = test_loader.discover('app/tests', pattern='test_*.py')
    
    # Run the tests
    test_runner = unittest.TextTestRunner(verbosity=2)
    result = test_runner.run(test_suite)
    
    # Exit with a non-zero code if any tests failed
    sys.exit(not result.wasSuccessful()) 