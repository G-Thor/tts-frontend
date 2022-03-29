"""
    TTS-text-process is a complete pipeline for preprocessing text for text-to-speech.

    Copyright (C) 2022 Grammatek ehf.

    This software is published under the Apache 2.0 License, sie LICENSE.
    Please note that submodules might be published under the MIT License (https://opensource.org/licenses/MIT)

    The Settings script for TTS-text-process ensures that all submodules are using the same dictionaries and
    character sets for the processing steps. While each module contains the data necessary for a stand-alone usage,
    it is important that all steps in the pre-processing pipeline use the same resources to avoid conflicts.

    To adapt the processing steps to your use case hence change this file and/or the corresponding files.

    Created: 03-2022
"""

import os
import logging
from .unicode_maps import replacement_dictionary, post_dict_lookup

# Set package path
package_path = os.path.dirname(os.path.abspath(__file__))

###########################
# Resource files
###########################
# This abbreviations file is extracted from DMII-abbreviations version 21.10, available here: http://hdl.handle.net/20.500.12537/164
# The file contains only unique entries, entries not used in the frontend-manager are commented out
DMII_ABBR_FILE = os.path.join(package_path, 'resources/dmii_abbr.txt')
# Abbreviations not included in the dmii-file
ABBR_FILE = os.path.join(package_path, 'resources/abbreviations_general.txt')
# Abbreviations that are very unlikely to stand at the end of a sentence
# (e.g. 'Dr.' which in a normal case should be followed by a name)
ABBR_NONENDING_FILE = os.path.join(package_path, 'resources/abbreviations_nonending.txt')
# The pronunciation dictionary used in the pipeline at each step to check for valid tokens.
# This is version 22.01, available here: http://hdl.handle.net/20.500.12537/181
PRON_DICT_FILE = os.path.join(package_path, 'resources/ice_pron_dict_standard_clear.csv')

##########################

# Replacement dictionary for unicode characters that should not 'make it' through text cleaning
CHAR_REPLACEMENT_DICT = replacement_dictionary
# Post processing, last check for characters to replace
POST_DICT = post_dict_lookup

# Characters valid throughout the pipeline. All other characters will be deleted or replaced in the text-cleaning
# module, except when they occur in tokens in valid dictionaries (abbreviations or pronunciation dictionaries)
# Note that the following characters from the English alphabet are not included: c, q, w, z
VALID_CHARACTERS = ['a', 'á', 'b', 'd', 'ð', 'e', 'é', 'f', 'g', 'h', 'i', 'í', 'j', 'k', 'l', 'm',
                      'n', 'o', 'ó', 'p', 'r', 's', 't', 'u', 'ú', 'v', 'y', 'ý', 'þ', 'æ', 'ö', 'x']

# punctuation symbols not deleted or replaced in the text-cleaner
PUNCTUATION = ['.',',',':','!','?', '/', '-']

# Default behaviour is to replace html closing tags with a full stop. Edit this map to change replacements
HTML_CLOSING_TAG_REPL = {
    'ul':'.',
    'ol':'.',
    'li':'.',
    'dl':'.',
    'dt':'.',
    'dd':'.',
    'table':'.',
    'tr':'.',
    'td':'.',
    'span':'.',
    'strong':'.',
    'h1':'.',
    'h2':'.',
    'h3':'.',
    'h4':'.',
    'h5':'.',
    'h6':'.',
    'p':'.',
    'br':'.',
    'hr':'.',
    'a':'', # leaving this empty helps with links broken in two between <a> tags
            # and plain text until books get better (html translators).
}


class ManagerResources:
    """ Holds lists and maps with lists and dictionaries for use in any submodule of the frontend manager.
        Lists of abbreviations and a pronunciation dictionary.
    """

    def __init__(self):
        self.abbreviations = self.read_lines([DMII_ABBR_FILE, ABBR_FILE])
        self.nonending_abbreviations = self.read_lines([ABBR_NONENDING_FILE])
        self.pron_dict = self.read_dict(PRON_DICT_FILE)

    @staticmethod
    def read_lines(file_list: list) -> set:
        """
        Reads lines from each of the files in file_list and appends to a set.
        Ignores empty lines.

        :param file_list: list of filenames to read from
        :return: a set containing all lines from the files in file_list
        """
        file_content = set()
        for fn in file_list:
            with open(fn) as f:
                for line in f.read().splitlines():
                    if not line:
                        continue
                    file_content.update(line.strip())
        return file_content

    @staticmethod
    def read_dict(filename: str) -> dict:
        """ Reads lines from 'filename' and initializes a dictionary. Logs a warning if a line in the file does
        not conform to the two column, tab separated format required; ignores empty lines.

        :param filename: the input file to read from
        :return: a dictionary with the file content
        """
        file_content = {}
        with open(filename) as f:
            for line in f.read().splitlines():
                if not line:
                    continue
                line_arr = line.split('\t')
                if len(line_arr) == 2:
                    file_content[line_arr[0]] = line_arr[1]
                else:
                    logging.warning(f'{line} in {filename} does not have the correct format (two tab separated columns)!')
        return file_content
