import re
import sys
import copy
import requests

"""
WIP
module = "CS1101S"

r = requests.get(f"https://api.nusmods.com/v2/{year}/modules/{module}.json")
if "prereqTree" in r.json().keys():
    print(r.json()["prereqTree"])
else:
    print("no prerequisites")

if "preclusion" in r.json().keys():
    x = re.findall("[A-Z]{2,3}\d{4}[A-Z]{0,}", r.json()["preclusion"])
else:
    print('no equivalents')

if "corequisite" in r.json().keys():
    x = re.findall("[A-Z]{2,3}\d{4}[A-Z]{0,}", r.json["corequisite"])
else:
    print('no equivalents')    


def recursive_prerequisites(module_list):
    global year
    final_list = dict()
    working_list = copy.deepcopy(module_list)
    checked = list()
    while working_list:
        current_module = working_list.pop()
        r = requests.get(f"https://api.nusmods.com/v2/{year}/modules/{current_module}.json")
"""

year = "2022-2023"

def add_modules(text):
    global year
    print(f"{text}\nEnter \"SUBMIT\" to submit.\nEnter a code again to remove it from the list.")
    modules = set()
    while True:
        for mods in modules:
            print(mods, sep='\t')
        x = input("Entry: ").upper()
        if x == "SUBMIT":
            break
        elif x in modules:
            modules.remove(x)
        else:
            if requests.get(f"https://api.nusmods.com/v2/{year}/modules/{x}.json").status_code == 200:
                modules.add(x)
                print(f"Removed {x}")
            else:
                print("Unrecognised module")
    return modules
