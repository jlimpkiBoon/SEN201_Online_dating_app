# file: utility.py
# purpose: Provide input validation utilities for handling numeric and non-empty user input.
# author: Boon
# date: 2025-09-29

import numbers

def check_number(question):
    """
    Prompt the user for a numeric input (integer or float) and validate it.

    This function repeatedly asks the user for input until a valid number is entered.
    It automatically detects whether the number should be treated as an integer or float.

    Args:
        question (str): The question or prompt displayed to the user.

    Returns:
        numbers.Number: The validated numeric input (either int or float).
    """
    while True:
        value = input(question).strip()
        if not value:
            print("Input cannot be blank. Please try again.")
            continue

        try:
            # Automatically detect integer or float
            if '.' in value:
                return float(value)
            else:
                return int(value)
        except ValueError:
            print("Invalid input. Please enter a valid number.")


def check_blank(question):
    """
    Prompt the user for a non-empty input string.

    This function continues to prompt the user until a non-blank response is given.

    Args:
        question (str): The question or prompt displayed to the user.

    Returns:
        str: The validated non-empty input string.
    """
    while True:
        answer = input(question).strip()
        if answer:
            return answer
        print("Input cannot be blank. Please try again.")

def press_enter_to_continue():
    """
    Pause program execution until the user presses Enter.

    This function is typically used to allow the user to read output
    before continuing to the next step in the program.

    Returns: None
    """
    input("\nPress Enter to continue...")

