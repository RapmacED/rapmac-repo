import csv
import io
import urllib.request
from typing import Dict, Any
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from time import sleep
import json
import pandas as pd

def main(params):
    # The file is available in the params dict keyed by param slug. url is the string URL where the file lives.
    url = params["file"]["url"]
    # Download from URL into memory
    response = urllib.request.urlopen(url)
    # Open the file as a CSV
    csv_file = csv.reader(io.TextIOWrapper(response))
    for row in csv_file:
        print(row)