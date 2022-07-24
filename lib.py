import re
import sys
import copy
import requests
from typing import *

YEAR = "2022-2023"

class Module:
    def __init__(self, code: str, prereq: List[str] = [], coreq: List[str] = []):
        self.code = code
        self.prereq = prereq
        self.coreq = coreq

def set_year(current_year) -> None:
    """
    Sets the year of NUS modules to explore
    :return: None
    """
    global YEAR
    YEAR = current_year

def parse_string(string) -> list[str]:
    """
    Returns a list of module codes from a string
    :return: List[String]
    """
    return re.findall("[A-Z]{2,3}\d{4}[A-Z]{0,}", string)

def obtain_prerequisites(module_code) -> set[Module]:
    """
    Returns a set of all prerequisites for a certain module or its equivalents
    :return: Set[Module]
    """
    global year
    prereqs = set()
    r = requests.get(f"https://api.nusmods.com/v2/{year}/modules/{module_code}.json")
    # Obtain the prerequisites directly from the module

    # Obtain the preclusions/equivalents of the module

    # From all the equivalents, obtain the prerequisites
    raise NotImplementedError

def generate_modules(module_list) -> set[Module]:
    """
    Generates a set of modules from a set of module codes
    :return: Set[Module]
    """
    global year
    final_list = set()
    working_list = copy.deepcopy(module_list)
    checked = list()
    while working_list:
        current_module = working_list.pop()
        r = requests.get(f"https://api.nusmods.com/v2/{year}/modules/{current_module}.json")
    raise NotImplementedError

def add_module_code(query) -> set[str]:
    """
    Generates a set of valid module code strings from user input
    :return: Set[String]
    """
    global year
    print(f"{query}\nEnter \"SUBMIT\" to submit.\nEnter a code again to remove it from the list.")
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
