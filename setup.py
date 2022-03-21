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


def gitcmd_update_submodules():
	'''	Check if the package is being deployed as a git repository. If so, recursively
		update all dependencies.

		@returns True if the package is a git repository and the modules were updated.
			False otherwise.
	'''
	if os.path.exists(os.path.join(here, '.git')):
		check_call(['git', 'submodule', 'update', '--init', '--recursive'])
		return True

	return False


class gitcmd_develop(develop):
	'''	Specialized packaging class that runs git submodule update --init --recursive
		as part of the update/install procedure.
	'''
	def run(self):
		gitcmd_update_submodules()
		develop.run(self)


class gitcmd_install(install):
	'''	Specialized packaging class that runs git submodule update --init --recursive
		as part of the update/install procedure.
	'''
	def run(self):
		gitcmd_update_submodules()
		install.run(self)


class gitcmd_sdist(sdist):
	'''	Specialized packaging class that runs git submodule update --init --recursive
		as part of the update/install procedure;.
	'''
	def run(self):
		gitcmd_update_submodules()
		sdist.run(self)

setup(
cmdclass={
		'develop': gitcmd_develop,
		'install': gitcmd_install,
		'sdist': gitcmd_sdist,
	},
    name='tts-textprocessing',
    version='0.1.21',

    description='A TTS text pre-processing pipeline for Icelandic',
    long_description=long_description,
    long_description_content_type='text/markdown',

    url='https://github.com/grammatek/tts-frontend',
    author='Grammatek ehf.',
    author_email='info@grammatek.com',

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
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        "Programming Language :: Python :: 3.10",
        'Programming Language :: Python :: 3 :: Only',
    ],

    keywords='text-processing, text-normalization, tokenizing, tts',

    package_dir={'': 'src'},
    packages=find_packages(where='src', exclude=['src/ice-g2p/src/ice_g2p/fairseq_models/standard/model-256-.3-s-s.pt']),

    python_requires='>=3.6, <4',

    # install_requires=['peppercorn'],  # check requirements!

    entry_points={
        'console_scripts': [
            'process=manager.textprocessing_manager:main',
        ],
    },
)
