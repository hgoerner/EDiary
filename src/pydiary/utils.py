"util modul"

import os


def first_util(num1: int, num2: int):
    """Returns the sum of two integers.

    This function takes two integer inputs and computes their sum, returning the result.
    It is a simple utility function for basic arithmetic operations.

    Args:
        num1 (int): The first integer to be added.
        num2 (int): The second integer to be added.

    Returns:
        int: The sum of num1 and num2.
    """

    return num1 + num2


def has_header(qmd_file):
    """Check if the .qmd file contains the Quarto YAML header."""
    if os.path.exists(qmd_file):
        with open(qmd_file, "r") as file:
            first_line = file.readline()
            return first_line.startswith("---")  # Check if the first line contains YAML start
    return False


def add_qmd_header(qmd_file):
    """Add the required Quarto YAML header to the .qmd file."""
    header = """---
title: "My Travel Diary"
format: 
  html:
    toc: true  # Enable table of contents for HTML
    toc-depth: 2
    embed-resources: true
    self-contained: true  # Include resources directly in the HTML output
    css: styles.css  # Link to a custom CSS file
execute:
  output: utf-8  # Setze die Ausgabe explizit auf UTF-8
---
"""
    with open(qmd_file, "w") as file:
        file.write(header)
    print("Added Quarto YAML header to the .qmd file.")
