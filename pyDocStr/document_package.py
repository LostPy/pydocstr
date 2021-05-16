import package_to_document

import pyDocStr

import os

print(pyDocStr.__file__)
current_path = os.getcwd()
print(current_path)
pyDocStr.build_docstrings_package(
									"./pyDocStr/package_to_document",
									new_package_path="./pyDocStr/package_documented",
									subpackages=True,
									level_logger='debug'
								)