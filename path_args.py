import os
from argparse import ArgumentParser


class PathArgs:
	def __init__(self, parser: ArgumentParser):
		self.parser = parser

	def create_args(self) -> None:
		self.parser.add_argument("output", metavar="O", type=str, help="folder to put edited gifs in")
		self.parser.add_argument("paths", metavar="P", type=str, nargs="+", help="paths to gifs")

	def check_args(self, args):
		if not all([path.split(".")[-1] == "gif" for path in args.paths]):
			self.parser.error("All paths must be gifs")

		if not os.path.isdir(args.output):
			self.parser.error("Output location must be a folder")
			