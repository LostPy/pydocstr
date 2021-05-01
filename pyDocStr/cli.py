import os
import argparse

from pyDocStr import create_docstrings_from_file, create_docstrings_from_folder


DESCRIPTION = ""


def create_parser():
	parser = argparse.ArgumentParser(description=DESCRIPTION)
	parser.add_argument('file', nargs='?', default=None,
						help='path of python file to document.',
						type=str)
	parser.add_argument('-d', '--directory', nargs='?', default=None,
						help="path of a directory to document.",
						type=str)
	parser.add_argument('--no-subdirs', action="store_true",
						help="If you wan't document subdirectories of directory passed to --directory argument")
	parser.add_argument('--decorator-name', nargs='?', default='to_document',
						help="The decorator name use for 'to_document' decorator.")
	parser.add_argument('-o', '--output', nargs='1', default=None,
						help="The output path, if not specify, the files are overwrite. The output must be a folder if --directory argument is passed else a file.",
						type=str)
	parser.add_argument('--formatter',  choices=['simple', 'numpy'], default='simple',
						help="The formatter to use if 'config' parameters is not specified.",
						type=str)
	parser.add_argument('--config', nargs='?', default=None,
						help='path of a config file for formatter.',
						type=str)
	parser.add_argument('--level-logger', choices=['debug', 'info', 'warning', 'error'],
						default='info', help="The logger level.")
	return parser


if __name__ == "__main__":
	parser = create_parser()
	args = parser.parse_args()

	print(args)