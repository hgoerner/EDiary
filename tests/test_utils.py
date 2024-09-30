import unittest
from pydiary.utils import has_header, add_qmd_header
import os


class TestUtils(unittest.TestCase):

    def test_has_header(self):
        # Create a temporary .qmd file with a header
        with open("temp_with_header.qmd", "w") as file:
            file.write("---\nheader content\n---\n")

        # Create a temporary .qmd file without a header
        with open("temp_without_header.qmd", "w") as file:
            file.write("no header content\n")

        self.assertTrue(has_header("temp_with_header.qmd"))
        self.assertFalse(has_header("temp_without_header.qmd"))

        # Clean up
        os.remove("temp_with_header.qmd")
        os.remove("temp_without_header.qmd")

    def test_add_qmd_header(self):
        # Create a temporary .qmd file
        temp_file = "temp.qmd"
        add_qmd_header(temp_file)

        with open(temp_file, "r") as file:
            content = file.read()

        expected_header = """---
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
        self.assertEqual(content, expected_header)

        # Clean up
        os.remove(temp_file)


if __name__ == "__main__":
    unittest.main()
