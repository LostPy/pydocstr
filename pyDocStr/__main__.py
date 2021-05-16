"""usage:  [-h] [-p [PACKAGE]] [--no-sub] [--decorator-name [DECORATOR_NAME]] [-o [OUTPUT]] [--formatter {simple,numpy}] [--config-formatter [CONFIG_FORMATTER]]
        [--level-logger {debug,info,warning,error}]
        [file]

A package to generate a complete documentation in your python files.

positional arguments:
  file                  path of python file to document.

optional arguments:
  -h, --help            show this help message and exit
  -p [PACKAGE], --package [PACKAGE]
                        path of a package to document. If this argument is used, a script to document the package is created.
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
"""
import sys
import os
import traceback
import argparse
import json
try:
	from yaml import YAMLError
except ModuleNotFoundError:
	class YAMLError(Exception):
		pass

import pyDocStr


DESCRIPTION = "A package to generate a complete documentation in your python files."


def create_parser():
	parser = argparse.ArgumentParser(description=DESCRIPTION)
	parser.add_argument('file', nargs='?', default=None,
						help='path of python file to document.',
						type=str)
	parser.add_argument('-p', '--package', nargs='?', default=None,
						help="path of a package to document. If this argument is used, a script to document is created.",
						type=str)
	parser.add_argument('--no-sub', action="store_true",
						help="If you wan't document subdirectories of directory passed to --directory argument  or subpackage of package passed to --package argument.")
	parser.add_argument('--decorator-name', nargs='?', default='to_document',
						help="The decorator name use for 'to_document' decorator.")
	parser.add_argument('-o', '--output', nargs='?', default=None,
						help="The output path, if not specify, the files are overwrite. The output must be a folder if --directory argument is passed else a file.",
						type=str)
	parser.add_argument('--formatter',  choices=['simple', 'numpy'], default='simple',
						help="The formatter to use if 'config' parameters is not specified.",
						type=str)
	parser.add_argument('--config-formatter', nargs='?', default=None,
						help='path of a config file for formatter.',
						type=str)
	parser.add_argument('--level-logger', choices=['debug', 'info', 'warning', 'error'],
						default='info', help="The logger level.")
	return parser


def get_code_to_document_package():
	return """
import pyDocStr

import {name}


pyDocStr.build_docstrings_package(
									{name},
									formatter={formatter},
									config_formatter={config_formatter},
									new_package_path={new_path},
									subpackages={subpackages},
									remove_decorator={remove_decorator},
									decorator_name={decorator_name},
									level_logger={level_logger}
								)
"""


def _get_str(str_: str) -> str:
	return "\"" + str_ + "\""


if __name__ == "__main__":
	parser = create_parser()
	args = parser.parse_args()

	pyDocStr.set_level_logger(args.level_logger)
	if args.config_formatter is None:
		formatter = pyDocStr.get_formatter(args.formatter)
	else:
		formatter = pyDocStr._formatter_from_config_path(args.config_formatter)
		if formatter is None:
			sys.exit(1)

	pyDocStr._logger.debug("debug mode - information on parameters")
	pyDocStr._logger.debug("-"*20)
	pyDocStr._logger.debug(f'current path: {os.getcwd()}')
	pyDocStr._logger.debug(f'file path: {args.file}')
	pyDocStr._logger.debug(f'package path: {args.package}')
	pyDocStr._logger.debug(f'no-sub: {args.no_sub}')
	pyDocStr._logger.debug(f'decorator-name: {args.decorator_name}')
	pyDocStr._logger.debug(f'formatter: {args.formatter}')
	pyDocStr._logger.debug(f'output: {args.output}')
	pyDocStr._logger.debug(f'config-formatter file: {args.config_formatter}')
	pyDocStr._logger.debug("-"*20)

	if args.package is None and args.file is not None:
		if os.path.exists(args.file):
			if args.output is not None and os.path.isdir(args.output):
				pyDocStr._logger.error(f"output argument must be a file, not a directory: '{args.output}'")
				sys.exit(1)
			pyDocStr.create_docstrings_from_module(args.file, formatter=formatter, new_path=args.output, decorator_name=args.decorator_name)

		else:
			pyDocStr._logger.error(f'The python file was not found: {args.file}')
			sys.exit(1)

	elif args.package is not None:
		if os.path.exists(args.package):
			if args.output is not None and os.path.isfile(args.output):
				pyDocStr._logger.error(f"output argument must be a directory, not a file: '{args.output}'")
				sys.exit(1)

			package = args.package.replace('\\', '/').rstrip('/')
			package_name = package.split('/')[-1]
			code = get_code_to_document_package()
			code = code.format(
				name=package_name,
				formatter=_get_str(args.formatter),
				new_path=_get_str(args.output) if args.output is not None else None,
				subpackages=not args.no_sub,
				decorator_name=_get_str(args.decorator_name),
				level_logger=_get_str(args.level_logger),
				remove_decorator=True,
				config_formatter=_get_str(args.config_formatter) if args.config_formatter is not None else None)

			name_script_to_document = f'script_to_document_{package_name}.py'
			path_script_to_document = os.path.join(os.path.dirname(package), name_script_to_document)
			with open(path_script_to_document, 'w') as f:
				f.write(code)
			pyDocStr._logger.warning(f"The script to document the package was created in '{path_script_to_document}'.")
			pyDocStr._logger.warning(f"Run the command: `python {name_script_to_document}` to document the package.")

	else:
		parser.print_help()
	sys.exit(0)	
