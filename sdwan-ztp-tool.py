import time

import eel
from tkinter import filedialog
from tkinter import *
from tkinter import *
from openpyxl import load_workbook
import json, requests, ipaddress, sys, platform, io

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

    sdwan_template_list = []
    polpkg_list = []

    std_objects = {
        "clitemplate": ["/pm/config/adom/$(adom_name)/obj/cli/template",
                        "/pm/config/adom/" + adomname + "/obj/cli/template", ["modification-time"]],
        "clitemplate-group": ["/pm/config/adom/$(adom_name)/obj/cli/template-group",
                              "/pm/config/adom/" + adomname + "/obj/cli/template-group", ["modification-time"]],
        "sdwaninterface": ["/pm/config/adom/$(adom_name)/obj/dynamic/virtual-wan-link/members/",
                           "/pm/config/adom/" + adomname + "/obj/dynamic/virtual-wan-link/members/",
                           ["dynamic_mapping", "obj seq"]],
        "sdwanservers": ["/pm/config/adom/$(adom_name)/obj/dynamic/virtual-wan-link/server/",
                         "/pm/config/adom/" + adomname + "/obj/dynamic/virtual-wan-link/server/",
                         ["dynamic_mapping"]],
        "sdwantemplates": ["/pm/wanprof/adom/$(adom_name)",
                           "/pm/wanprof/adom/" + adomname,
                           ["scope member", "oid"]],
        "addrobjs": ["pm/config/adom/$(adom_name)/obj/firewall/address/",
                     "pm/config/adom/" + adomname + "/obj/firewall/address/",
                     ["uuid", "dynamic_mapping"]],
        "addrobjs_grp": ["pm/config/adom/$(adom_name)/obj/firewall/addrgrp/",
                         "pm/config/adom/" + adomname + "/obj/firewall/addrgrp/",
                         ["uuid", "dynamic_mapping"]],
        "intfobjs": ["pm/config/adom/$(adom_name)/obj/dynamic/interface/",
                     "pm/config/adom/" + adomname + "/obj/dynamic/interface/",
                     ["uuid", "dynamic_mapping"]],
        "applist": ["pm/config/adom/$(adom_name)/obj/application/list",
                    "pm/config/adom/" + adomname + "/obj/application/list",
                    ["uuid", "dynamic_mapping", "obj seq"]],
        "appgrp": ["pm/config/adom/$(adom_name)/obj/application/group",
                   "pm/config/adom/" + adomname + "/obj/application/group",
                   ["uuid", "dynamic_mapping", "obj seq"]],
        "service": ["pm/config/adom/$(adom_name)/obj/firewall/service/custom",
                    "pm/config/adom/" + adomname + "/obj/firewall/service/custom",
                    ["uuid", "dynamic_mapping", "obj seq"]],
        "servicegrp": ["pm/config/adom/$(adom_name)/obj/firewall/service/group",
                       "pm/config/adom/" + adomname + "/obj/firewall/service/group",
                       ["uuid", "dynamic_mapping", "obj seq"]],
        "polpkg": ["pm/pkg/adom/$(adom_name)",
                   "pm/pkg/adom/" + adomname,
                   ["scope member", "oid"]]

    }

    for objecturls in std_objects:
        get_and_add(std_objects, objecturls)

    ## Get SDWAN Template Details
    for sdwan_template in sdwan_template_list:
        get_and_add({"sdwan_member": [
            "pm/config/adom/$(adom_name)/wanprof/" + sdwan_template + "/system/virtual-wan-link/member",
            "pm/config/adom/" + adomname + "/wanprof/" + sdwan_template + "/system/virtual-wan-link/member",
            ["obj seq"]]}, "sdwan_member")

        get_and_add({"sdwan_hlth": [
            "pm/config/adom/$(adom_name)/wanprof/" + sdwan_template + "/system/virtual-wan-link/health-check",
            "pm/config/adom/" + adomname + "/wanprof/" + sdwan_template + "/system/virtual-wan-link/health-check",
            ["obj seq"]]}, "sdwan_hlth")

        get_and_add({"sdwan_service": [
            "pm/config/adom/$(adom_name)/wanprof/" + sdwan_template + "/system/virtual-wan-link/service",
            "pm/config/adom/" + adomname + "/wanprof/" + sdwan_template + "/system/virtual-wan-link/service",
            ["obj seq"]]}, "sdwan_service")

    ## Get Policy Package Details
    for polpkg in polpkg_list:
        get_and_add({"polpkg_policy": ["pm/config/adom/$(adom_name)/pkg/" + polpkg + "/firewall/policy",
                                       "pm/config/adom/" + adomname + "/pkg/" + polpkg + "/firewall/policy",
                                       ["obj seq", "_policy_block"]]}, "polpkg_policy")

    # print(json.dumps(export_info, indent=4, sort_keys=True))
    return json.dumps(export_info, indent=4, sort_keys=True)
