import re

from utils import *
from typing import *


class ModuleGraph:
    API_ENDPOINT: str = "https://api.nusmods.com/v2/"
    YEAR: str = "2022-2023"

    def __init__(self, endpoint: str, year: str):
        try:
            r = requests.get(endpoint)
        except requests.ConnectionError | requests.HTTPError:
            raise ValueError("There might be an error with your Internet Connection or with the API Endpoint input")
        else:
            if r.status_code == 200:
                self.API_ENDPOINT = endpoint
            else:
                raise ValueError("Invalid URL")

        if re.match(r"\d{4}-\d{4}", year):
            self.YEAR = year
        else:
            raise ValueError(r"Year input does not match the required year input format (\d{4}-\d{4})")

        self.GRAPH: Dict[Module, List[Module]] = {}

    def __str__(self):
        return str(self.GRAPH)

    def __repr__(self):
        return str(self.GRAPH)

    # ----- Verifiers ----- #
    @staticmethod
    def parse_module_code(module_code: str):
        """Parses the module code and checks if it is a valid module code"""

        return re.match(r"[A-Z]{2,3}\d{4}[A-Z]{0,}", module_code)

    # ----- Graph Building Functions ----- #
    def add_module_node(self, module: Module):
        """Adds a module as a Node in the Graph"""
        if module not in self.GRAPH:
            self.GRAPH[module] = []

    def add_module_edge(self, module_origin: Module, module_destination: Module):
        """
        Adds a module Edge in the graph, linking the origin module to the destination module

        For the purposes of module dependency tree building, you are not allowed to associate an origin module with
        the destination module, and a list of Nodes connected to a particular node cannot contain the particular node
        in the list
        """

        if module_origin is module_destination or module_origin == module_destination:
            raise ValueError("Module cannot be associated with itself or with an equivalent module")
        elif module_origin not in self.GRAPH:
            self.GRAPH[module_origin] = [module_destination]
        else:
            self.GRAPH.get(module_origin).append(module_destination)

    # ----- API Request and Parsing ----- #
    def send_request(self, module_code: str) -> dict or None:
        """
        Public method that sends a request to the API endpoint with a specific module and returns a Python dictionary
        containing the details of the request
        """

        if not isinstance(module_code, str) and not self.parse_module_code(module_code):
            raise TypeError("Module Code must be a string, and match the format of a Module Code")

        url = self.API_ENDPOINT + self.YEAR + "/modules/" + module_code + ".json"

        try:
            r = requests.get(url)
            r.raise_for_status()
        except requests.ConnectionError as e:
            self.parse_error_codes(e, "Connection to API failed. Check your Internet connection and/or your "
                                      "API Endpoint")
        except requests.HTTPError as e:
            self.parse_error_codes(e, f"Invalid URL: {url}")
        else:
            return r.json()

    def get_tree(self, module: str):
        if self.parse_module_code(module):
            r = self.send_request(module)
            all_modules = {
                "prerequisite": None,
                "preclusion": None,
                "corequisite": self.get_corequisites(module)
            }

    def get_corequisites(self, module: str):
        """Returns the corequisites of a module"""

        if self.parse_module_code(module):
            r = self.send_request(module)

            if "corequisite" in r.keys():
                return [mod for mod in self.parse_string(r.get("corequisite"))]
        else:
            raise ValueError("Module code is not in the correct format")

    def get_preclusions(self, module: str):
        """Returns a list of preclusions of an input module"""

        if self.parse_module_code(module):
            pass
        else:
            raise ValueError("Module code is not in the correct format")

    def get_prerequisites(self, module: str):
        """Returns a list of prerequisities of an input module"""

        pass

    def remove_deeply_from_graph(self, module: Module):
        """
        Remove a particular module deeply from the graph if it is found in it

        Node list takes precendence over the edge lists in the graph, and is checked first before the edges are checked
        """

        if module in self.GRAPH:
            del self.GRAPH[module]

        for node in self.GRAPH:
            if module in self.GRAPH[node]:
                self.GRAPH[node].remove(module)
                break
