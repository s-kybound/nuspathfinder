from lib import *
from defaults import *
from typing import *

from InquirerPy import inquirer
from InquirerPy.validator import *
from InquirerPy.base.control import Choice
from pyfiglet import Figlet
from termcolor import cprint


class CLIApp:
    """
    Class that modularize the process of gathering inputs from the user and places into functions that can be reused

    Calling the constructor of this class will start the app and direct all outputs to stdout
    """

    def __init__(self, ascii_colour: Literal["grey", "red", "green", "yellow", "blue", "magenta", "cyan",
                                             "white"] = "blue",
                 font: Literal["3-d", "alphabet", "banner3", "slant", "barbwire", "block", "doom", "isometric1",
                               "ogre", "standard", "speed"] = "slant"):
        self.ASCII_ART_COLOUR = ascii_colour
        self.ASCII_ART_FONT = font
        self.FIGLET_DEFAULT = Figlet(font=self.ASCII_ART_FONT)
        self.SELECTED = []
        self.welcome_screen()

    def welcome_screen(self) -> None:
        """
        Welcome screen for the CLI Application

        :return: None
        """

        cprint(self.FIGLET_DEFAULT.renderText("Pathfinder"), color="blue")
        cprint("Welcome to the NUS Pathfinder App!\n"
               "Build Version: v0.0\n\n"
               "Made with ❤️ by Kyriel\n", color="blue")

        # entry point that invokes all other function
        self.course_selection()

    def course_selection(self) -> None:
        """
        Selects the course the user wants to plan out

        :raise: ValueError, if the user attempts to override the option selection enforced by the CLI
        :return: None, options are chained
        """

        course_selector = inquirer.select(
            message="Please select your course to begin:",
            choices=[
                "Computer Science, Standalone",
                "Computer Science, with 2nd Degree/Major/Minor",
                "Custom",
                "Quit"
            ],
            default="Computer Science, Standalone"
        ).execute(raise_keyboard_interrupt=True)

        match (course_selector):
            case "Computer Science, Standalone":
                self.SELECTED.extend(COMPUTER_SCIENCE_CORE_MODS)
                self.SELECTED.extend(COMPUTER_SCIENCE_MATH_MODS)
                self.data_literacy_selection()
            case "Computer Science, with 2nd Degree/Major/Minor":
                self._not_implemented()
            case "Custom":
                self.custom_modules()
            case "Quit":
                self.quit()
            case _:
                raise ValueError("Unrecognised Command")

    def data_literacy_selection(self) -> None:
        """
        Function to query what Data Literacy mod the user wants to take

        :return: None
        """

        data_lit_selector = inquirer.select(
            message="Select a Data Literacy Mod:",
            choices=[
                "GEA1000",
                "BT1101",
                "ST1131",
                "DSE1101",
                "Go Back",
                "Quit"
            ],
            default="GEA1000"
        ).execute(raise_keyboard_interrupt=True)

        match (data_lit_selector):
            case "GEA1000" | "BT1101" | "ST1131" | "DSE1101":
                self.SELECTED.append(data_lit_selector)
                self.custom_modules()
            case "Go Back":
                self.course_selection()
            case "Quit":
                self.quit()
            case _:
                raise ValueError("Unrecognised Command")

    def custom_modules(self):
        """
        Function to query the custom modules to be taken by the user

        :return: None
        """

        custom_mod_selector = inquirer.select(
            message="Custom Mode: ",
            choices=[
                "Add Modules",
                "Go Back",
                "Skip to Specialisation",
                "Quit"
            ],
            default="Add Modules"
        ).execute(raise_keyboard_interrupt=True)

        match (custom_mod_selector):
            case "Add Modules":
                self.custom_modules_adder()
            case "Go Back":
                self.welcome_screen()
            case "Quit":
                self.quit()
            case "Skip to Specialisation":
                self.specialisation_modules()
            case _:
                raise ValueError("Unrecognised Command")

    def custom_modules_adder(self):
        """
        Function which repeatedly prompt user for input for Custom modules

        :return: None
        """

        input_mod = inquirer.text("Key in a Core/Foundation Module for your course (key in Q to quit): ").execute()
        if input_mod:
            if input_mod == "Q":
                cprint("Terminating Module Addition Mode...", "red")
                self.custom_modules()
            else:
                self.SELECTED.append(input_mod)
                self.custom_modules_adder()

    def specialisation_modules(self):
        """
        Function to query the specialisation/track modules to be taken by the user

        :return: None
        """

        spec_selector = inquirer.select(
            message="Specialisation Module Mode:",
            choices=[
                "Add Modules",
                "Go Back",
                "Skip to UE Modules",
                "Quit"
            ],
            default="Add Modules"
        ).execute(raise_keyboard_interrupt=True)

        match (spec_selector):
            case "Add Modules":
                self.specialisation_modules_adder()
            case "Go Back":
                self.custom_modules()
            case "Quit":
                self.quit()
            case "Skip to UE Modules":
                self.ue_modules()
            case _:
                raise ValueError("Unrecognised Command")

    def specialisation_modules_adder(self):
        """
        Function which repeatedly prompt user for input for specialisation/track modules

        :return: None
        """

        input_mod = inquirer.text("Add all 4-MC modules in your specialisation/track(s) that you intend to take "
                                  "(key in Q to quit): ")\
            .execute()
        if input_mod:
            if input_mod == "Q":
                cprint("Terminating Module Addition Mode...", "red")
                self.custom_modules()
            else:
                self.SELECTED.append(input_mod)
                self.custom_modules_adder()

    def ue_modules(self):
        """
        Function to query the unrestricted elective modules to be taken by the user

        :return: None
        """

        spec_selector = inquirer.select(
            message="Unrestricted Elective Module Mode:",
            choices=[
                "Add Modules",
                "Go Back",
                "Finalise",
                "Quit"
            ],
            default="Add Modules"
        ).execute(raise_keyboard_interrupt=True)

        match (spec_selector):
            case "Add Modules":
                self.ue_modules_adder()
            case "Go Back":
                self.specialisation_modules()
            case "Finalise":
                self.finalise()
            case "Quit":
                self.quit()
            case _:
                raise ValueError("Unrecognised Command")

    def ue_modules_adder(self):
        """
        Function which repeatedly prompt user for input for unrestricted elective modules

        :return: None
        """

        input_mod = inquirer.text("Add all remaining 4-MC modules, such as remaining GE/RC4 modules"
                                  "(key in Q to quit): ") \
            .execute()
        if input_mod:
            if input_mod == "Q":
                cprint("Terminating Module Addition Mode...", "red")
                self.custom_modules()
            else:
                self.SELECTED.append(input_mod)
                self.custom_modules_adder()

    def finalise(self):
        """
        Prints out a summary of the modules the user has chosen

        :return: None
        """

        cprint("\n##### Summary #####", "cyan")
        mc_credit = len(self.SELECTED) * 4
        cprint(f"Number of MCs: {mc_credit} / 160", "cyan")
        cprint(f"Modules Taken: {self.SELECTED}", "cyan")
        if (mc_credit <= 160):
            cprint("Status: {Viable}", "green")
        else:
            cprint("Status: {Not Viable}", "red")

    def _not_implemented(self):
        """Utility function which tells users that the functionality has not been implemented yet"""

        cprint("Sorry the feature is not implemented yet!", "red")

    def quit(self):
        """Exits the program after alerting the user"""

        cprint("Command received, exiting...", "red")
        exit(0)
