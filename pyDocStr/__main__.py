"""usage: pyDocStr [-h] [-d [DIRECTORY]] [--no-subdirs] [--decorator-name [DECORATOR_NAME]] [-o [OUTPUT]] [--formatter {simple,numpy}] [--config-formatter [CONFIG_FORMATTER]]
                   [--level-logger {debug,info,warning,error}]
                   [file]

A package to generate a complete documentation in your python files.

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
	parser.add_argument('-d', '--directory', nargs='?', default=None,
						help="path of a directory to document.",
						type=str)
	parser.add_argument('-p', '--package', nargs='?', default=None,
						help="path of a package to document.",
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
	pyDocStr._logger.debug(f'folder path: {args.directory}')
	pyDocStr._logger.debug(f'package path: {args.package}')
	pyDocStr._logger.debug(f'no-sub: {args.no_sub}')
	pyDocStr._logger.debug(f'decorator-name: {args.decorator_name}')
	pyDocStr._logger.debug(f'formatter: {args.formatter}')
	pyDocStr._logger.debug(f'output: {args.output}')
	pyDocStr._logger.debug(f'config-formatter file: {args.config_formatter}')
	pyDocStr._logger.debug("-"*20)

	if args.directory is None and args.package is None and args.file is not None:
		if os.path.exists(args.file):
			if args.output is not None and os.path.isdir(args.output):
				pyDocStr._logger.error(f"output argument must be a file, not a directory: '{args.output}'")
				sys.exit(1)
			pyDocStr.create_docstrings_from_module(args.file, formatter=formatter, new_path=args.output, decorator_name=args.decorator_name)

		else:
			pyDocStr._logger.error(f'The python file was not found: {args.file}')
			sys.exit(1)

	elif args.package is None and args.directory is not None:
		if os.path.exists(args.directory):
			if args.output is not None and os.path.isfile(args.output):
				pyDocStr._logger.error(f"output argument must be a directory, not a file: '{args.output}'")
				sys.exit(1) 

			pyDocStr.create_docstrings_from_folder(args.directory, formatter=formatter, new_folderpath=args.output,
													subfolders=not args.no_sub, decorator_name=args.decorator_name)
		else:
			pyDocStr._logger.error(f'The directory was not found: {args.directory}')
			sys.exit(1)

	elif args.package is not None:
		if os.path.exists(args.package):
			if args.output is not None and os.path.isfile(args.output):
				pyDocStr._logger.error(f"output argument must be a directory, not a file: '{args.output}'")
				sys.exit(1)
			pyDocStr.create_docstrings_from_package(args.package, formatter=formatter, new_package_path=args.output,
													subpackages=not args.no_sub, decorator_name=args.decorator_name)
	else:
		parser.print_help()
	sys.exit(0)	
