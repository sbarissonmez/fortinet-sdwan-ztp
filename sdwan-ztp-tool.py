import time

import eel
from tkinter import filedialog
from tkinter import *
from tkinter import *
from openpyxl import load_workbook
import json
import requests
import ipaddress
import sys
import platform
import io

requests.packages.urllib3.disable_warnings()

# Set web files folder and optionally specify which file types to check for eel.expose()
#   *Default allowed_extensions are: ['.js', '.html', '.txt', '.htm', '.xhtml']
eel.init('web', allowed_extensions=['.js', '.html'])
