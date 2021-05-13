# pydocstr

A package to generate a complete documentation in your python files.


## Index

 1. Global Informations
 2. Requirements
 3. Installation
 4. Quickly start
 5. Use with config formatter file

## Global Informations

 * Author: LostPy
 * Date: 2021-04-25
 * Version: 1.0.5 (2021-05-13)

## Requirements

 * Optional:
 	 * [colorama][colorama]: for color logs
   * [yaml][yaml]: to read yaml file

## Installation

To install this package, use : `pip install git+https://github.com/LostPy/pydocstr.git@stable`

## Quickly start

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

### List options

|name|optional|Description|Value|Default|
|:--:|:------:|-----------|:---:|:-----:|
|`file`|✅|The path of python file to document (If `--directory` is not used.|A path (str)|`None`|
|`--directory`|✅|The path of a folder to document|A path (str)|`None`|
|`--package`|✅|The path of a package to document|A path (str)|`None`|
|`--no-sub`|✅|Specifies that sub-directories or sub-packages should not be documented|||
|`--decorator-name`|✅|To specify the decorator name use for `to_document` decorator. It's used to remove decorators `to_document`.|A str|`to_document`|
|`--output`|✅|If a file is specified, this is the path where the new source code should be saved. If directory option is specified, must be the path of folder where the news source code should be saved.|A path (str)|The new source code is saved in the old file.|
|`--formatter`|✅|The formatter to use for the docstring format.|`simple` or `numpy`|`simple`|
|`--config-formatter`|✅|A file with the configuration for a custom formatter.|A path (str)|`None`|
|`--level-logger`|✅|The level of logger.|`debug`, `info`, `warning` or `error`|`info`|

> ⚠️ **All parameters are optional**, if there is neither a file nor a directory specified, the help message is displayed.

> ⚠️ If there is **a file and a directory specified**, only the specified directory is documented.

### Help

The help message
```
usage:  [-h] [-d [DIRECTORY]] [-p [PACKAGE]] [--no-sub] [--decorator-name [DECORATOR_NAME]] [-o [OUTPUT]] [--formatter {simple,numpy}] [--config-formatter [CONFIG_FORMATTER]]
        [--level-logger {debug,info,warning,error}]
        [file]

A package to generate a complete documentation in your python files.

positional arguments:
  file                  path of python file to document.

optional arguments:
  -h, --help            show this help message and exit
  -d [DIRECTORY], --directory [DIRECTORY]
                        path of a directory to document.
  -p [PACKAGE], --package [PACKAGE]
                        path of a package to document.
  --no-sub              If you wan't document subdirectories of directory passed to --directory argument or subpackage of package passed to --package argument.
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

## Use with a configuration file

### The config file

The config file can be a json or a yaml file if the yaml module is installed.

> ℹ️ **Note:** To install the yaml module, use: `python install pyyaml`

The configuration file must have the following 6 keywords:

|name|type|description|keywords|
|:--:|:--:|-----------|--------|
|`description`|*str*|The description format for docstrings|`description`|
|`fields`|*str*|The format of a field in docstring (fields = `Parameters`, `Returns`...)|`name`, `items`, `prefix`, `suffix`|
|`items`|*str*|The item format, an item is an element of a field (parameter...)|`name`, `description`, `type`, `default`|
|`prefix`|*str*|The prefix of name field use. The prefix is repeated so that it has the same length as the field name.||
|`suffix`|*str*|The suffix of name field use. The suffix is repeated so that it has the same length as the field name.||

> ⚠️ **Keywords must be specified between `{}`**: `"{keyword}"`

> ℹ️ **Note:** The keywords can be `null` to use the default value.

Example of a config file with a **yaml file**:

```YAML
# The format for the description of a function or a class. The key word '{description}' is mandatory.
description: "{description}\n"

# The format of a field in docstring ('Parameters', 'Returns'...).
fields: "{prefix}\n{name}\n{suffix}\n{items}"

# The format of a item in a field (a parameter...).
items: "{name} : {type}\n\t{description}\n\t{default}"

# The prefix use for fields. Use only if 'prefix' key word is use in 'fields'.
# This prefix is repeated so that it has the same length as the field name.
prefix: ''

# The suffix use for fields. Use only if 'suffix' key word is use in fields.
# This suffix is repeated so that it has the same length as the field name.
suffix: '-'  # With the field 'Parameters', this prefix give '----------' (10*'-')
```

Example of a config file with a **json file**:
```json
{
  "description": "{description}\n",
  "fields": "{prefix}\n{name}\n{suffix}\n{items}",
  "items": "{name} : {type}\n\t{description}\n\t{default}",
  "prefix": "",
  "suffix": "-"
}
```

### Command line

To document all functions and class decorated with `to_document` decorator from `module_to_document.py`, use: `python -m pyDocStr ./module_to_document.py --config-formatter ./config.json`

[colorama]: https://pypi.org/project/colorama/
[yaml]: https://pypi.org/project/PyYAML/