import re
import sys
import copy
import unittest
import requests
from typing import *

class TestStringMethods(unittest.TestCase):
    def test_set_year(self):
        global YEAR
        set_year("2019-2020")
        self.assertEqual(YEAR, "2019-2020")
        self.assertNotEqual(YEAR, "2022-2023")
        set_year("2022-2023")

    def test_parse_string(self):
        self.assertEqual(
            parse_string("Hello friends CS1010"),
            ["CS1010"])
        self.assertEqual(
            parse_string("Hello friends MA1301FC"),
            ["MA1301FC"])
        self.assertEqual(
            parse_string("Hello friends M1301FC"),
            [])
        self.assertEqual(
            parse_string("Hello friends MA131FC"),
            [])
        self.assertEqual(
            parse_string("Hello friends MA131FC"),
            [])
        self.assertEqual(
            parse_string("CS1010 CS1101S MA1301FC"),
            ["CS1010", "CS1101S", "MA1301FC"])


YEAR = "2022-2023"

class Module:
    def __init__(self, code: str, prereq: Set[str] = [], coreq: Set[str] = []):
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

def parse_string(string) -> List[str]:
    """
    Returns a list of module codes from a string
    :return: List[String]
    """
    return re.findall("[A-Z]{2,3}\d{4}[A-Z]{0,}", string)

def obtain_prerequisites(module_code) -> Set[str]:
    """
    Returns a set of all prerequisites for a certain module or its equivalents
    :return: Set[str]
    """
    prereqs = set()
    r = requests.get(f"https://api.nusmods.com/v2/{YEAR}/modules/{module_code}.json")
    # Obtain the prerequisites directly from the module

    # Obtain the preclusions/equivalents of the module

    # From all the equivalents, obtain the prerequisites

    raise NotImplementedError

def generate_modules(module_list) -> Set[Module]:
    """
    Generates a final set of modules from a set of module codes
    :return: Set[Module]
    """
    final_list = set()
    working_list = copy.deepcopy(module_list)
    checked = list()
    while working_list:
        current_module = working_list.pop()
        if current_module not in checked:
            r = requests.get(f"https://api.nusmods.com/v2/{YEAR}/modules/{current_module}.json")

    raise NotImplementedError

def add_module_code(query) -> Set[str]:
    """
    Generates a set of valid module code strings from user input
    :return: Set[String]
    """
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

if __name__ == "__main__":
    print("Running tests for lib.py")
    unittest.main()