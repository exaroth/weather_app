#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
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

    def __init__(self, config):
        self.config = config

    def get_location(self):
        addr_req = requests.get("http://freegeoip.net/json")
        return addr_req.json()

    def parse_request(self, location, system, **kwargs):

        addr = self.API
        if not system:
            system = "metric"
        addr += "?q={0}&units={1}".format(location, system)
        return addr

    def process_request(self, address):

        try:
            req = requests.get(address)
            return req.json()
        except requests.HTTPError as e:
            print("Unable to retrieve weather data from remote server\n\
                  Error:{0}".format(str(e)))


    def get_info(self):
        if "location" not in self.config.keys():
            try:
                loc = self.get_location()
            except Exception as e:
                print("Unable to retrieve location data from freegeoip.net,\n\
                        Enter your location manually or try again.")
        else:
            loc = self.config["location"]
        request_address = self.parse_request(loc, self.config.get("system", None))
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
        if key in ("l", "--location"):
            config["location"] = val
        if key in ("s", "--system"):
            config["system"] = val
        if key in ("a", "--additional_fields"):
            config["additional"] = val
    w = WeatherApp(config)
    w.get_info()

main()
