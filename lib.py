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
        eqv1 = obtain_prerequisites("CS2030S")
        eqv2 = {obtain_preclusions("CS1010")}
        self.assertEqual(eqv1, eqv2)
        # Test CS2030, which should return the same as CS2030S
        eqv3 = obtain_prerequisites("CS2030")
        self.assertEqual(eqv1, eqv3)
        # Test CS1010 which has no prerequisites
        self.assertEqual(obtain_prerequisites("CS1010"), set())
        # Test CS1010LOL, which doesn't exist and so should return an empty set
        self.assertEqual(obtain_prerequisites("CS1010LOL"), set())

    def test_obtain_preclusions(self):
        # Test CS1010 and all of its preclusions
        self.assertEqual(
            obtain_preclusions("CS1010"),
            Or({"CS1010", "CS1010E", "CS1010J", "CS1010S", "CS1010X", "CS1010XCP", "CS1101S", "CS1010FC"}))
        # Test CS2104 which has no preclusions
        self.assertEqual(obtain_preclusions("CS2014"), set())
        # Test CS1010LOL, which doesn't exist and so should return an empty set
        self.assertEqual(obtain_preclusions("CS1010LOL"), set())

    def test_obtain_corequisites(self):
        # Test CS2101, which has corequisite CS2103T
        self.assertEqual(obtain_corequisites("CS2101"), {"CS2103T"})
        # Test CS1010, which has no corequisites
        self.assertEqual(obtain_corequisites("CS1010"), set())

    def test_generate_modules(self):
        self.assertEqual(
            generate_modules({"CS1101S", "CS2030S"}),
            {Module("CS1101S"), Module("CS2030S")})

    def test_evaluate_modules(self):
        # First test CS1101S. Since there are no prerequisites, this should return an empty list
        self.assertEqual(
            evaluate_modules(generate_modules({"CS1101S"})),
            set())
        # Now test CS2040S. There should be 2 sets of misssing prerequisites
        self.assertEqual(
            evaluate_modules(generate_modules({"CS2040S"})),
            set({obtain_preclusions("CS1231S"), obtain_preclusions("CS1101S")}))
        # Now test CS2040S and CS1101S. There should only be one missing prerequisite set, CS1231S
        self.assertEqual(
            evaluate_modules(generate_modules({"CS2040S", "CS1101S"})),
            set({obtain_preclusions("CS1231S")}))
 
YEAR = "2022-2023"

class Or:
    def __init__(self, preclus: FrozenSet[str] = frozenset()):
        self.preclus = frozenset(preclus)

    def __eq__(self, other):
        return self.preclus == other.preclus

    def __hash__(self):
        return hash(self.preclus)

class Module:
    def __init__(self, code: str, prereqs: Set[Or] = set(), preclus = Or, coreqs: Set[str] = set()):
        self.code = code
        self.prereqs = prereqs
        self.preclus = preclus
        self.coreqs = coreqs

    def __eq__(self, other):
        return self.code == other.code

    def __hash__(self):
        return hash(self.code)

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
    :return: List[str]
    """
    return re.findall("[A-Z]{2,3}\d{4}[A-Z]{0,}", string)

def obtain_prerequisites(module_code) -> Set[Or]:
    """
    Returns a set of all prerequisites for a certain module or its equivalents
    :return: Set[Or]
    """
    prereqs = set()
    r = requests.get(f"https://api.nusmods.com/v2/{YEAR}/modules/{module_code}.json")
    if r.status_code == 404:
        return set()
    # Obtain the prerequisites directly from the module
    if "prerequisite" in r.json().keys():
        for mod in parse_string(r.json()["prerequisite"]):
            for or_set in prereqs:
                if mod in or_set.preclus:
                    continue
            mod_preclus = obtain_preclusions(mod)
            if not mod_preclus:
                continue
            prereqs.add(mod_preclus)
    # From all the equivalents, obtain the prerequisites
    equivalents = obtain_preclusions(module_code)
    if equivalents:
        equivalents = set(equivalents.preclus)
        while equivalents:
            current_working_module = equivalents.pop()
            s = requests.get(f"https://api.nusmods.com/v2/{YEAR}/modules/{current_working_module}.json")
            if s.status_code == 404:
                continue
            if "prerequisite" in s.json().keys():
                for mod in parse_string(s.json()["prerequisite"]):
                    for or_set in prereqs:
                        if mod in or_set.preclus:
                            continue
                    mod_preclus = obtain_preclusions(mod)
                    if not mod_preclus:
                        continue
                    prereqs.add(mod_preclus)
    return prereqs

def obtain_preclusions(module_code) -> Or:
    """
    Returns a set of all preclusions, or equivalents, of a module
    :return: Or
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
    return Or(explored)

def obtain_corequisites(module_code) -> Set[str]:
    """
    Returns a set of all corequisites of a module
    :return: Set[str]
    """
    r = requests.get(f"https://api.nusmods.com/v2/{YEAR}/modules/{module_code}.json")
    if r.status_code == 404:
        return set()
    coreqs = set()
    if "corequisite" in r.json().keys():
        for mod in parse_string(r.json()["corequisite"]):
            coreqs.add(mod)
    # Corequisite modules are much stricter and may not allow equivalents, hence we only use direct results
    return coreqs

def generate_modules(module_list) -> Set[Module]:
    """
    Generates a final set of modules from a set of module codes
    :return: Set[Module]
    """
    module_set = set()
    for mod in module_list:
        module_set.add(
            Module(
                code = mod,
                prereqs = obtain_prerequisites(mod),
                preclus = obtain_preclusions(mod),
                coreqs = obtain_corequisites(mod)))
    return module_set

def evaluate_modules(module_set) -> Set[Or]:
    """
    Evaluates a set of modules. If all prerequisites have been met, indicate
    that the set is valid, else list it as invalid, and list and return all
    the sets of missing prerequisites
    :return: Set[Or]
    """
    working_set = copy.deepcopy(module_set)
    missing = set()
    while working_set:
        current_module = working_set.pop()
        current_prerequisites = current_module.prereqs
        for or_set in current_prerequisites:
            in_set = False
            # Check if every Or in the prerequisite is fulfilled
            for prereq in or_set.preclus:
                for mod in module_set:
                    if mod.code == prereq:
                        in_set = True
            if not in_set:
                missing.add(or_set)
    return missing

def add_module_code(query) -> Set[str]:
    """
    Generates a set of valid module code strings from user input
    :return: Set[str]
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
