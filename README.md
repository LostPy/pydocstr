# pydocstr

A package to generate a complete documentation in your python files.


## Index

 1. Global Informations
 2. Requirements
 3. Installation

## Global Informations

 * Author: LostPy
 * Date: 2021-04-25
 * Version: 1.0.1 (2021-05-01)

## Requirements

 * Optionnal:
 	* [colorama][colorama]: for color logs

## Installation

To install this package, use : `pip install git+https://github.com/LostPy/pydocstr.git@stable`

## Quickly use

To document a python file or a folder with pythons files, there are three steps:
 1. In python files to document, import `pyDocStr` with `to_document` decorator
 2. Decorate with `to_document` all functions, methods and class which must be documented. You can specify a description in decorator.
 3. Execute `python -m pyDocStr`

> ⚠️ **To document methods of a class**, the **class must be decorated** with `to_document` decorator (and all methods which must be decorated).

### Add docstring to a file

To document a file, use the command: `python -m pyDocStr path/of/your/file_to_document.py`

Example with `module_to_document.py`:
```py
from pyDocStr import to_document


@to_document(description='A function which print these arguments.')
def function_one(arg1, arg2: int, arg3: str, arg4: float = 1.):
	print(arg1, arg2, arg3, arg4)


@to_document(description='A function wich return a tuple.')
def function_two() -> tuple:
	return (0, 0)
```

In the same folder than the file: `python -m pyDocStr ./module_to_document.py -o ./module_documented.py`

### Add docstring to pythons files of a folder

To document all python files of a folder, use: `python -m pyDocStr -d path/of/your/folder`.  
If you wan't documented the subfolders, use: `python -m pyDocStr -d path/of/your/folde --no-subdirs`.

### Help

The help message
```
usage: pyDocStr [-h] [-d [DIRECTORY]] [--no-subdirs] [--decorator-name [DECORATOR_NAME]] [-o [OUTPUT]] [--formatter {simple,numpy}] [--config-formatter [CONFIG_FORMATTER]]
                   [--level-logger {debug,info,warning,error}]
                   [file]

positional arguments:
  file                  path of python file to document.

optional arguments:
  -h, --help            show this help message and exit
  -d [DIRECTORY], --directory [DIRECTORY]
                        path of a directory to document.
  --no-subdirs          If you wan't document subdirectories of directory passed to --directory argument
  --decorator-name [DECORATOR_NAME]
                        The decorator name use for 'to_document' decorator.
  -o [OUTPUT], --output [OUTPUT]
                        The output path, if not specify, the files are overwrite. The output must be a folder if --directory argument is passed else a file.
  --formatter {simple,numpy}
                        The formatter to use if 'config' parameters is not specified.
  --config-formatter [CONFIG_FORMATTER]
                        path of a config file for formatter.
  --level-logger {debug,info,warning,error}
                        The logger level.

```

[colorama]: https://pypi.org/project/colorama/