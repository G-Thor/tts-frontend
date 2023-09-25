"""TTS text preprocessing pipeline

Copyright (C) 2022 Grammatek ehf.

License: Apache 2.0 (see: LICENSE)
This package uses 3rd party submodules that might be published under other comparable open licenses.

This module sets up the TTS textprocessing package and installs the 'process' command-line utility.
"""
import os, pathlib

from setuptools.command.develop import develop
from setuptools.command.install import install
from setuptools.command.sdist import sdist
from setuptools import setup, find_packages
from subprocess import check_call


here = pathlib.Path(__file__).parent.resolve()

long_description = (here / 'README.md').read_text(encoding='utf-8')
setup(
    name='icefrontend',
    version='0.2.0',

    description='A TTS text pre-processing pipeline for Icelandic',
    long_description=long_description,
    long_description_content_type='text/markdown',

    url='https://github.com/G-Thor/tts-frontend',
    author='Grammatek ehf., Reykjavik University',
    author_email='info@grammatek.com, gunnaro@ru.is',

    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering',
        'Topic :: Software Development',
        'Topic :: Text Processing :: Linguistic',
        'Natural Language :: Icelandic',
        'License :: OSI Approved :: Apache Software License',

        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        "Programming Language :: Python :: 3.10",
        'Programming Language :: Python :: 3 :: Only',
    ],

    keywords='text-processing, text-normalization, tokenizing, tts',

    include_package_data=True,
    package_dir={'': 'src'},
    packages=find_packages(where='src'),
    python_requires='>=3.8, <4',

    # check requirements!
    install_requires=[
        'pos @ git+https://github.com/cadia-lvl/POS@4b44be9',
        'text-cleaner @ git+https://github.com/grammatek/text-cleaner@34b9c130a39142e83ced2383e0b65d66a27c53d9',
        'reynir-correct >= 3.4.6',
    ],


    entry_points={
        'console_scripts': [
            'process=icefrontend.textprocessing_manager:main',
        ],
    },
)
