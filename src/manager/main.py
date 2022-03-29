#!/usr/bin/env python
"""

    TTS-text-process is a complete pipeline for preprocessing text for text-to-speech.

    Copyright (C) 2022 Grammatek ehf.

    This software is published under the Apache 2.0 License, sie LICENSE.
    Please note that submodules might be published under the MIT License (https://opensource.org/licenses/MIT)

    This is the entry point to the execution of the whole pipeline, single modules may be evoked from each
    manager (cleaner_manager, normalizer_manager, etc.). The main() function of this module is registered as
    a console_script entry point in setup.py

"""
from .tokens_manager import extract_text
from .textprocessing_manager import Manager


def get_example_text():
    return 'Snýst í suðaustan 10-18 m/s og hlýnar með rigningu, en norðaustanátt og snjókoma NV-til fyrri part dags. '


def process(text: str) -> str:
    return text


def process_to_json(text: str) -> str:
    return text

def main():
    manager = Manager()
    input_text = get_example_text()
    clean = manager.clean(input_text)
    print("============== CLEAN TOKENS =======================")
    print(clean)
    print(extract_text(clean))
    normalized = manager.normalize(clean)
    print("============== NORMALIZED TOKENS ==================")
    print(normalized)
    phrased = manager.phrase(normalized)
    for token in phrased:
        print(token)
    transcribed = manager.transcribe(phrased)
    for token in transcribed:
        print(token)
    print(extract_text(transcribed, False))


if __name__ == '__main__':
    main()