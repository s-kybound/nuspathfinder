import re
import requests

from utils import *
from typing import *


class Parser:
    API_ENDPOINT: str = "https://api.nusmods.com/v2/"
    YEAR: str = "2022-2023"

    def __init__(self, year: Optional[str] = None, endpoint: Optional[str] = None,
                 alert_level: ConnectionAlertLevel = ConnectionAlertLevel.LOG):
        self.YEAR = self.YEAR if (not year and not isinstance(year, str)) else year
        self.API_ENDPOINT = self.API_ENDPOINT if (not endpoint and not isinstance(endpoint, str)) else endpoint
        self.alert_level = alert_level

    @property
    def year(self):
        """Year property"""

        return self.YEAR

    @year.setter
    def year(self, v: str):
        """Sets the value of the year of the running instance of the Parser"""

        if isinstance(v, str) and re.match(r"\d{4}-\d{4}", v):
            self.YEAR = v
        else:
            raise TypeError(f"Cannot set year to {v}")

    @property
    def endpoint(self):
        """API Endpoint property"""

        return self.API_ENDPOINT

    @endpoint.setter
    def endpoint(self, v: str):
        """Sets the value of the global API endpoint for the running instance of the Parser"""

        if isinstance(v, str) and re.match(r"https://\w*", v):
            self.API_ENDPOINT = v
        else:
            raise TypeError(f"Cannot set API Endpoint to {v}")

    @staticmethod
    def parse_string(string: str, regex: Optional[str] = None) -> List[str] or None:
        """
        Public method that allows users to parse a string into a list of matches for modules
        Returns a list of module codes from a given string using regex expressions

        Parameters
        ----------
        :param string:          The string to parse and return matches for
        :param regex:           An optional regex string that overrides the built in module regex pattern
        """

        return re.findall(r"[A-Z]{2,3}\d{4}[A-Z]{0,}", string) if not regex else re.findall(regex, string)

    @staticmethod
    def parse_module_code(module_code: str):
        """Parses the module code and checks if it is a valid module code"""

        return re.match(r"[A-Z]{2,3}\d{4}[A-Z]{0,}", module_code)

    def parse_error_codes(self, exception: Exception, logger_string: str):
        """A function that parses the incoming exception according to the alert level set by the class"""

        if self.alert_level == ConnectionAlertLevel.RAISE:
            raise exception
        elif self.alert_level == ConnectionAlertLevel.LOG:
            print(logger_string)
        elif self.alert_level == ConnectionAlertLevel.SUPPRESS:
            pass

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

    def prerequisite(self, module_code: str):
        """Conducts a DFS to find all dependencies for a given module"""

        if not self.parse_module_code(module_code):
            raise TypeError("Module Code must be of the correct format")

        prerequisite = []
        preclusions = self.preclusion(module_code)
        equivalents = list(preclusions)
        running = [module_code]
        completed = []

        while running:
            curr_module = running.pop()
            r = self.send_request(curr_module)

            if r is not None and "prerequisite" in r.keys():
                for module in self.parse_string(r.get("prerequisite")):
                    if module in completed:
                        continue
                    else:
                        if module not in preclusions:
                            preclusions.update(self.preclusion(module))

                        completed.append(module)

        while equivalents:
            curr_module = equivalents.pop()
            cm_requests = self.send_request(curr_module)
            if cm_requests is None:
                continue

            if cm_requests is not None and "prerequisite" in cm_requests.keys():
                for mod in self.parse_string(cm_requests.get("prerequisite")):
                    for or_set in prerequisite:
                        if mod not in or_set.preclus:
                            mod_preclus = self.preclusions(mod)
                            if not mod_preclus:
                                continue
                            prerequisite.add(mod_preclus)

        return prerequisite

    def preclusion(self, module_code: str) -> Set:
        """Conducts a BFS to find all precluded modules in the chain"""

        if not self.parse_module_code(module_code):
            raise TypeError("Module Code must be of the correct format")

        to_check = [module_code]
        completed = []
        precluded = []

        while to_check:
            curr_mod = to_check.pop()
            if curr_mod in completed:
                continue

            r = self.send_request(curr_mod)
            if r is not None and "preclusion" in r.keys():
                for mod in self.parse_string(r["preclusion"]):
                    to_check.append(mod)
                    precluded.append(mod)

            completed.append(curr_mod)

        return set(precluded)

    def corequisites(self, module_code: str) -> Set[str]:
        """Returns a set of corequisite modules for a particular input module"""
        r = self.send_request(module_code)

        if "corequisite" in r.keys():
            return set([mod for mod in self.parse_string(r.get("corequisite"))])

        return set()

    def return_modules(self, module_list) -> Set[Module]:
        """Parses a list of module code and return the Module representation of each module"""

        return set([Module(
            code=m,
            prerequisites=self.prerequisite(m),
            preclusions=self.preclusion(m),
            corequisites=self.corequisites(m)) for m in module_list])


if __name__ == '__main__':
    parser = Parser()
    print(parser.preclusion("CS1101S"))
    print(parser.prerequisite("MA2001"))
