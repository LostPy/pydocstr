from setuptools import setup, find_packages

import pyDocStr

__doc__ = """A package and a parser to document pythons files quickly."""


setup(
	name='pyDocStr',
	version='1.0.6',
	author='LostPy',
	description="A package to document pythons files.",
	long_description=__doc__,
    package_dir = {'pyDocStr': './pyDocStr'},
    package_data = {'': ['LICENSE.txt', 'requirements.txt']},
	include_package_data=True,
	url='https://github.com/LostPy/pydocstr',
	classifiers=[
        "Programming Language :: Python",
        "Development Status :: Functionnal",
        "License :: MIT",
        "Natural Language :: French",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.5+"
    ],
    license='MIT',
    packages = find_packages()
    )