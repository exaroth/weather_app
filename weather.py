#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This is a simple script for getting weather information
from remote server(openweathermap.org in this case)
"""

from __future__ import print_function
import requests
import json
import sys
import os
import getopt

__version__ = "0.0.1"
__author__ = "Konrad Wasowicz"
__license__ = "BSD"


class WeatherApp(object):
    
    """
    Main class for getting weather information
    """

    API = "http://api.openweathermap.org/data/2.5/weather"

    def __init__(self, config):
        self.config = config

    def get_location(self):

        # Get location based on ip address
        # Not very reliable

        addr_req = requests.get("http://freegeoip.net/json")
        return addr_req.json()

    def parse_request(self, location, system, **kwargs):

        # Parse address to be used in request

        addr = self.API
        if not system:
            system = "metric"
        addr += "?q={0}&units={1}".format(location, system)
        return addr

    def process_request(self, address):

        # Process and return the response

        try:
            req = requests.get(address)
            return req.json()
        except requests.HTTPError as e:
            print("Unable to retrieve weather data from remote server\n\
                  Error:{0}".format(str(e)))


    def get_info(self):

        # Main method for returning weather information

        if "location" not in self.config.keys():
            try:
                loc = self.get_location()
                location = loc["city"] or loc["region_name"] or loc["country_name"]
            except Exception as e:
                print("Unable to retrieve location data from freegeoip.net,\n Enter your location manually or try again.")
        else:
            location = self.config["location"]
        request_address = self.parse_request(location, self.config.get("system", None))
        response = self.process_request(request_address)
        print("Location:", response["name"])
        print("Weather: ", response["weather"][0]["main"])
        print("Temperature: ", response["main"]["temp"], u"\u00b0" + "C")
        print("Humidity", response["main"]["humidity"])

def main():

    args = sys.argv[1:]

    config = dict()

    try:
        options, remainder = getopt.getopt(args,"l:a:s:", ["location=", "system=", "additional_fields="])
    except getopt.GetoptError as err:
        sys.exit(2)

    for field in options:
        key, val = field
        if key in ("-l", "--location"):
            config["location"] = val
        if key in ("-s", "--system"):
            config["system"] = val
        if key in ("-a", "--additional_fields"):
            config["additional"] = val
    w = WeatherApp(config)
    w.get_info()

main()
