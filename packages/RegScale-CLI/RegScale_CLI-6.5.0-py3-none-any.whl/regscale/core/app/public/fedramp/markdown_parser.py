"""
This module contains the MDDocParser class, which is used to parse an SSP Appendix A file
and return a dictionary representing the data in the markdown document.
"""

import re
import logging
import zipfile  # Assuming you need this for other file handling
import pypandoc
from collections import defaultdict
from typing import Dict, TextIO, Optional, Tuple
from regscale.models import ProfileMapping

# Configure logger
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Tokens used in HTML parsing
BEGINPARTTOKEN = "<tr>"
ENDPARTTOKEN = "</tr>"
BODYSTARTTOKEN = "<tbody>"
BODYENDTOKEN = "</tbody>"
CONTROLSUMMARYTOKEN = "What is the solution"


def clean_part(part: str) -> str:
    """
    Cleans an HTML part string by removing specific HTML tags.

    :param part: The HTML part string
    :return: A cleaned HTML part string with specific tags removed
    """
    # Pattern to match specified HTML tags, using non-capturing groups for better performance
    pattern = re.compile(r"</?(td|tr|th|tbody|thead)(?: [^>]*)?>", re.IGNORECASE)
    return pattern.sub("", part).strip()


class MDDocParser:
    """
    Parses an SSP .md file and extracts control parts into a dictionary.
    """

    def __init__(self, md_path: str, profile_id: int):
        """
        Initializes the MDDocParser with the path to the markdown file.

        :param str md_path: Path to the markdown file
        :param int profile_id: The profile ID to associate with the control parts
        """
        # List of controls to parse
        self.md_path = md_path
        try:
            self.controls = [profile_map.controlId for profile_map in ProfileMapping.get_by_profile(profile_id)]
            # Convert .md file to markdown_strict format and save output
            self.md_text = pypandoc.convert_file(md_path, "markdown_strict", outputfile="app_a.md")
            self.md_doc = "app_a.md"
        except Exception as e:
            logger.error(f"Error converting file: {e}")
            raise

    def get_parts(self) -> Dict[str, str]:
        """
        Parses the .md file and extracts control parts.

        :return: A dictionary of control parts, keyed by control ID
        """
        control_parts_dict = defaultdict(str)
        try:
            with open(self.md_doc, "r") as file:
                for line in file:
                    if CONTROLSUMMARYTOKEN in line:
                        control_id = self._handle_control_summary_line(line)
                        if not control_id:
                            continue
                        # Skip lines to find the table content
                        next(file)  # Skip HTML table definition line
                        # Loop through file to capture parts between tbody tags
                        self.find_parts(file, control_parts_dict, control_id)
        except FileNotFoundError as e:
            logger.error(f"File not found: {e}")
        except Exception as e:
            logger.error(f"Error parsing file: {e}")
        return control_parts_dict

    def _handle_control_summary_line(self, line: str) -> Optional[str]:
        """
        Handles a line of text from the markdown file.

        :param str line: The line of text
        :return: The control ID
        :rtype: Optional[str]
        """
        # Extract control ID and clean it
        line_items = line.split(" ")
        control_id = None
        # Assuming line_items and self.controls are already defined
        for line_item in line_items:
            # Find the first control that matches a line_item
            control_id = next((control for control in self.controls if control in line_item), None)
            # If a matching control ID is found, break out of the loop
            if control_id:
                break
        return control_id

    def find_parts(self, file: TextIO, control_parts_dict: Dict, cntrlid: str):
        """
        Parses and collects parts from a markdown file into a dictionary by control ID.

        :param file: The markdown file
        :param control_parts_dict: Dictionary to store parts by control ID
        :param cntrlid: The control ID
        """
        allparts = ""
        for line in file:
            if BODYSTARTTOKEN in line:
                continue
            elif BODYENDTOKEN in line:
                break
            allparts += self.part_cleaner(file, line)

        control_parts_dict[cntrlid] = allparts
        logger.debug(f"Control ID: {cntrlid}, Parts: {allparts}")

    @staticmethod
    def part_cleaner(file: TextIO, line: str) -> str:
        """
        Cleans and accumulates parts of text from the markdown file.

        :param file: The markdown file
        :param line: The current line of text
        :return: The cleaned part as a string
        """
        part = ""
        for next_line in file:
            part += clean_part(next_line)
            if ENDPARTTOKEN in next_line:
                break
        return part
