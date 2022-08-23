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

"""
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
"""
setup(
#cmdclass={
#		'develop': gitcmd_develop,
#		'install': gitcmd_install,
#		'sdist': gitcmd_sdist,
#	},
    name='tts-textprocessing',
    version='0.1.24',

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

    include_package_data=True,
    package_dir={'': 'src'},
    packages=find_packages(where='src'),
    python_requires='>=3.6, <4',

    # check requirements!
    install_requires=[
        'text-cleaner @ git+https://github.com/grammatek/text-cleaner@34b9c130a39142e83ced2383e0b65d66a27c53d9',
        'regina_normalizer @ git+https://github.com/grammatek/regina_normalizer@01da6cb4a2e6ba8e5935cd1339723c17526ad820',
        'reynir-correct @ git+https://github.com/grammatek/GreynirCorrect4LT@af29c41a58f64dbbe5e2c2610c0d426338c3048f',
        'ice-g2p @ git+https://github.com/grammatek/ice-g2p@bc145b77b92cf1f05edd69fc54f7cced8877f471',
        'phrasing-tool @ git+https://github.com/grammatek/phrasing-tool@50537e5880816340dce8b63ebc7a86dd3407cbeb'
    ],


    entry_points={
        'console_scripts': [
            'process=manager.textprocessing_manager:main',
        ],
    },
)
