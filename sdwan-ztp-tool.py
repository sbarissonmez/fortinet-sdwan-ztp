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

def sendupdate(return_html):
    eel.pageupdate(return_html)

### Export ADOM Functions
def export_adom(adomname):
    global export_info
    global sdwan_template_list
    global polpkg_list
    export_info = {"vars": ["adom_name", "adom_desc"], "settings": []}
    requestid = 1

    ## Get ADOM Info
    newdict = {"url": "/dvmdb/adom/", "method": "add", "data": []}

    jsondata = {
        "method": "get",
        "params": [
            {
                "url": "/dvmdb/adom/" + adomname
            }

        ],
        "id": requestid,
        "session": fmg_sessionid
    }
    res = session.post(fmgurl, json=jsondata, verify=False)
    parsed = json.loads(res.text)
    # print(json.dumps(parsed, indent=4, sort_keys=True))

    dvmdbadom = parsed['result'][0]['data']
    dvmdbadom.pop('uuid', None)
    dvmdbadom.pop('oid', None)
    dvmdbadom["name"] = "$(adom_name)"
    dvmdbadom["desc"] = "$(adom_desc)"
    if adomname == "root":
        dvmdbadom["flags"] = 2312

    newdict["data"].append(dvmdbadom)
    export_info["settings"].append(newdict)

    ## standard objects (objects which can be exported and imported with out changing anything, mutliple objects can be created in a list)
