import re
import sys
import copy
import requests

from typing import *

MODULE = "CS1101S"
YEAR = "2022-2023"
# "[A-Z]{2,3}\d{4}[A-Z]{0,}"


class Module:
    def __init__(self, code: str, prereq: List[str] = [], coreq: List[str] = []):
        self.code = code
        self.prereq = prereq
        self.coreq = coreq


def recursive_prerequisites(module_list: List[Module]):
    final_list = dict()
    working_list = copy.deepcopy(module_list)
    checked = list()
    while working_list:
        current_module = working_list.pop()
        r = requests.get(f"https://api.nusmods.com/v2/{YEAR}/modules/{current_module}.json")


def add_modules(text: str):
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
            print(f"Removed {x}")
        else:
            if requests.get(f"https://api.nusmods.com/v2/{YEAR}/modules/{x}.json").status_code == 200:
                modules.add(x)
            else:
                print("Unrecognised module")
    return modules
