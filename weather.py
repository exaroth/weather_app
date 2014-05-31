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

    API = "http://api.openweathermap.org/data/2.5/"

    def __init__(self, config, **kwargs):
        self.config = config
        if self.config.get("system") == "imperial":
            self.config["measure"] = "F"
        else:
            self.config["measure"] = "C"
        if "location" not in config.keys():
            try:
                self.location = self.get_location()
            except Exception as e:
                print("Unable to retrieve location data from freegeoip.net,\n Enter your location manually or try again.")
        else:
            self.location = self.config["location"]
        print(kwargs)
        if "forecast" in kwargs.keys() and kwargs.get("forecast") is not None:
            self.forecast_count = kwargs["forecast"]

    def get_location(self):

        # Get location based on ip address
        # Not very reliable

        addr_req = requests.get("http://freegeoip.net/json")
        loc = addr_req.json()

        return loc["city"] or loc["region_name"] or loc["country_name"]

    def parse_request_addr(self, system, forecast = False):

        # Parse address to be used in request

        addr = self.API
        if forecast:
            addr += "forecast/daily"
        else:
            addr += "weather"
        if not system:
            system = "metric"
        addr += "?q={0}&units={1}".format(self.location, system)
        if forecast:
            addr += "&cnt={0}&mode=json".format(self.forecast_count)
        print(addr)
        return addr

    def process_request(self, address):

        # Process and return the response

        try:
            req = requests.get(address)
            return req.json()
        except requests.HTTPError as e:
            print("Unable to retrieve weather data from remote server\n\
                  Error:{0}".format(str(e)))


    def get_weather_for_today(self):

        # Main method for returning weather information

        request_address = self.parse_request_addr(self.config.get("system", None))
        response = self.process_request(request_address)
        print("Location:", response["name"])
        print("Weather: ", response["weather"][0]["main"])
        print("Temperature: ", response["main"]["temp"], u"\u00b0" + self.config["measure"] )
        print("Humidity", response["main"]["humidity"])

    def get_forecast(self):

        request_address = self.parse_request_addr(self.config.get("system", None), forecast=self.forecast_count)
        response = self.process_request(request_address)
        print(response)

def main():
    args = sys.argv[1:]

    config = dict()

    try:
        options, remainder = getopt.getopt(args,"l:a:s:f:", ["location=", "system=", "additional_fields=", "forecast="])
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
        if key in ("-f", "--forecast"):
            forecast = val
    w = WeatherApp(config, forecast = forecast)
    w.get_forecast()

main()
