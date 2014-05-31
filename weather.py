#!/bin/env python

import requests
import json
import sys
import os
import getopt

__version__ = "0.0.1"
__author__ = "Konrad Wasowicz"
__license__ = "BSD"


req = requests.get("http://api.openweathermap.org/data/2.5/weather?q=London,uk&units=metric&")



class WeatherApp(object):

    API = "http://api.openweathermap.org/data/2.5/weather"

    def __init__(self):
        pass

    def get_location(self):
        pass

    def parse_request(self):
        pass

    def get_data(self):
        pass

    def get_info(self):
        pass


def main():

    args = sys.argv[1:]

    if len(args) > 0:
        pass

    weather = WeatherApp()
    





