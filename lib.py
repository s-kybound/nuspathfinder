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
            parse_string("Hello friends MA1301HELLo"),
            ["MA1301HELL"])
        self.assertEqual(
            parse_string("Hello friends M1301FC"),
            [])
        self.assertEqual(
            parse_string("Hello friends MA131FC"),
            [])
        self.assertEqual(
            parse_string("Hello friends MA131HELLO"),
            [])
        self.assertEqual(
            parse_string("CS1010 CS1101S MA1301FC"),
            ["CS1010", "CS1101S", "MA1301FC"])
        self.assertEqual(
            parse_string("CS1010, Ma1301b, MA1301C and others"),
            ["CS1010", "MA1301C"])

    def test_obtain_prerequisites(self):
        # Test CS2030S which should return all the different CS1010 variants
        eqv1 = []
        eqv2 = ["CS1010"]
        for mod in obtain_prerequisites("CS2030S"):
            eqv1.append(mod)
        for mod in obtain_preclusions("CS1010"):
            eqv2.append(mod)
        eqv1.sort()
        eqv2.sort()
        self.assertEqual(eqv1, eqv2)
        # Test CS2030, which should return the same as CS2030S
        eqv3 = []
        for mod in obtain_prerequisites("CS2030"):
            eqv3.append(mod)
        eqv3.sort()
        self.assertEqual(eqv1, eqv3)
        # Test CS1010 which has no prerequisites
        self.assertEqual(obtain_prerequisites("CS1010"), set())
        # Test CS1010LOL, which doesn't exist and so should return an empty set
        self.assertEqual(obtain_prerequisites("CS1010LOL"), set())

    def test_obtain_preclusions(self):
        # Test CS1010 and all of its preclusions
        eqv1 = []
        eqv2 = ["CS1010E", "CS1010FC", "CS1010J", "CS1010S", "CS1010X", "CS1010XCP", "CS1101S"]
        for mod in obtain_preclusions("CS1010"):
            eqv1.append(mod)
        eqv1.sort()
        eqv2.sort()
        self.assertEqual(eqv1, eqv2)
        # Test CS2104 which has no preclusions
        self.assertEqual(obtain_preclusions("CS2014"), set())
        # Test CS1010LOL, which doesn't exist and so should return an empty set
        self.assertEqual(obtain_preclusions("CS1010LOL"), set())

    def test_generate_modules(self):
        self.assertEqual(
            generate_modules({"CS1101S", "CS2030S"}),
            {Module("CS1101S"), Module("CS2030S")})

YEAR = "2022-2023"

class Module:
    def __init__(self, code: str, prereq: Set[str] = [], coreq: Set[str] = []):
        self.code = code
        self.prereq = prereq
        self.coreq = coreq
    def __eq__(self, other):
        return self.code == other.code

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
    if r.status_code == 404:
        return set()
    # Obtain the prerequisites directly from the module
    if "prerequisite" in r.json().keys():
        for mod in parse_string(r.json()["prerequisite"]):
            prereqs.add(mod)
    # From all the equivalents, obtain the prerequisites
    equivalents = obtain_preclusions(module_code)
    while equivalents:
        current_working_module = equivalents.pop()
        s = requests.get(f"https://api.nusmods.com/v2/{YEAR}/modules/{current_working_module}.json")
        if s.status_code == 404:
            continue
        if "prerequisite" in s.json().keys():
            for mod in parse_string(s.json()["prerequisite"]):
                if mod in prereqs:
                    continue
                prereqs.add(mod)
    # Now search for preclusions of the prerequisites themselves
    action_set = copy.deepcopy(prereqs)
    while action_set:
        current_working_module = action_set.pop()
        for mod in obtain_preclusions(current_working_module):
            if mod in prereqs:
                continue
            prereqs.add(mod)
            action_set.add(mod)
    return prereqs

def obtain_preclusions(module_code) -> Set[str]:
    """
    Returns a set of all preclusions, or equivalents, of a module
    :return: Set(str)
    """
    r = requests.get(f"https://api.nusmods.com/v2/{YEAR}/modules/{module_code}.json")
    if r.status_code == 404:
        return set()
    explored = {module_code}
    if "preclusion" in r.json().keys():
        action_set = set()
        for mod in parse_string(r.json()["preclusion"]):
            action_set.add(mod)
        # Search for additional preclusions in action_set till depleted
        while action_set:
            current_working_module = action_set.pop()
            if current_working_module in explored:
                continue
            explored.add(current_working_module)
            s = requests.get(f"https://api.nusmods.com/v2/{YEAR}/modules/{current_working_module}.json")
            if s.status_code == 404:
                continue
            if "preclusion" in s.json().keys():
                for mod in parse_string(s.json()["preclusion"]):
                    if mod in explored:
                        continue
                    action_set.add(mod)
    # explored serves as the set of preclusions, hence remove module code itself
    explored.remove(module_code)
    return explored

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
