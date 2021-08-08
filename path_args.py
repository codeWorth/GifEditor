import os
from argparse import ArgumentParser


class PathArgs:
	@staticmethod
	def create_args(parser: ArgumentParser) -> None:
		parser.add_argument("output", metavar="O", type=str, help="folder to put edited gifs in")
		parser.add_argument("paths", metavar="P", type=str, nargs="+", help="paths to gifs")

	@staticmethod
	def check_args(self, parser: ArgumentParser, args) -> None:
		if not all([path.split(".")[-1] == "gif" for path in args.paths]):
			parser.error("All paths must be gifs")

		if not os.path.isdir(args.output):
			parser.error("Output location must be a folder")
			