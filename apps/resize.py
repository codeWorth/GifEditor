from PIL.Image import Image
import argparse
from editor import ImageOp
from path_args import PathArgs
from typing import Iterator


class ResizeArgs:
	@staticmethod
	def create_args(parser: argparse.ArgumentParser) -> None:
		parser.add_argument("-W", "--width", type=int, help="output width in pixels")
		parser.add_argument("-H", "--height", type=int, help="output height in pixels")
		parser.add_argument("--scale_width", type=float, help="output width scale as a float")
		parser.add_argument("--scale_height", type=float, help="output height scale as a float")
		parser.add_argument("-S", "--scale", type=float, help="output scale as a float")

	@staticmethod
	def check_args(parser: argparse.ArgumentParser, args) -> None:
		has_pixel_size = args.width or args.height
		has_scale = args.scale_width or args.scale_height
		has_aspect_scale = bool(args.scale)

		if has_pixel_size and has_scale:
			parser.error("Cannot have absolute size and scaled size")

		if has_pixel_size and has_aspect_scale:
			parser.error("Cannot have absolute size and scaled size")

		if has_scale and has_aspect_scale:
			parser.error("Cannot have scaled size and aspect scaled size")

		if bool(args.scale_width) ^ bool(args.scale_height):
			parser.error("Must have both --scale_width and --scale_height parameters present")


class ResizeOp(ImageOp):
	def __init__(self, width: int, height: int):
		self.width = width
		self.height = height

	def get_edited_frames(self, frames: Iterator[Image]) -> Iterator[Image]:
		for image in frames:
			yield image.resize((self.width, self.height))

	def op_type(self) -> str:
		return "resize"


class AspectResizeOp(ImageOp):
	def __init__(self, width: int = None, height: int = None):
		self.width = width
		self.height = height

	def get_edited_frames(self, frames: Iterator[Image]) -> Iterator[Image]:
		for image in frames:
			if self.width:
				self.height = int(image.size[1] * self.width / image.size[0])
			elif self.height:
				self.width = int(image.size[0] * self.height / image.size[1])
			yield image.resize((self.width, self.height))

	def op_type(self) -> str:
		return "resize, maintaining aspect ratio"


class ScaleOp(ImageOp):
	def __init__(self, width_scale: float, height_scale: float):
		self.width_scale = width_scale
		self.height_scale = height_scale

	def get_edited_frames(self, frames: Iterator[Image]) -> Iterator[Image]:
		for image in frames:
			width = image.size[0] * self.width_scale
			height = image.size[1] * self.height_scale
			yield image.resize((int(width), int(height)))

	def op_type(self) -> str:
		return "resize w/ scale"


class AspectScaleOp(ImageOp):
	def __init__(self, scale: float):
		self.scale = scale

	def get_edited_frames(self, frames: Iterator[Image]) -> Iterator[Image]:
		for image in frames:
			width = image.size[0] * self.scale
			height = image.size[1] * self.scale
			yield image.resize((int(width), int(height)))

	def op_type(self) -> str:
		return "resize w/ scale, maintaining aspect ratio"

	
def make_parser() -> argparse.ArgumentParser:
	parser = argparse.ArgumentParser(description="Resize gifs with given paths.")
	PathArgs.create_args(parser)
	ResizeArgs.create_args(parser)
	return parser

if __name__ == "__main__":
	parser = make_parser()
	args = parser.parse_args()
	PathArgs.check_args(parser, args)
	ResizeArgs.check_args(parser, args)

	if args.width and args.height:
		for path in args.paths:
			ResizeOp(args.width, args.height).edit_gif(path, args.output)
	elif args.width:
		for path in args.paths:
			AspectResizeOp(width=args.width).edit_gif(path, args.output)
	elif args.height:
		for path in args.paths:
			AspectResizeOp(height=args.height).edit_gif(path, args.output)
	elif args.scale_width:
		for path in args.paths:
			ScaleOp(args.scale_width, args.scale_height).edit_gif(path, args.output)
	elif args.scale:
		for path in args.paths:
			AspectScaleOp(args.scale).edit_gif(path, args.output)
	else:
		raise TypeError("Unknown resizing type")
