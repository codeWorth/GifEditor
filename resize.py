from PIL import Image
import argparse, os
from editor import ImageOp


class ResizeOp(ImageOp):
	def __init__(self, width: int, height: int):
		self.width = width
		self.height = height

	def apply(self, image: Image) -> Image:
		return image.resize((self.width, self.height))

	def op_type(self) -> str:
		return "resize"


class AspectResizeOp(ImageOp):
	def __init__(self, width: int = None, height: int = None):
		self.width = width
		self.height = height

	def apply(self, image: Image) -> Image:
		if self.width:
			self.height = int(image.size[1] * self.width / image.size[0])
		elif self.height:
			self.width = int(image.size[0] * self.height / image.size[1])
		return image.resize((self.width, self.height))

	def op_type(self) -> str:
		return "resize, maintaining aspect ratio"


class ScaleOp(ImageOp):
	def __init__(self, width_scale: float, height_scale: float):
		self.width_scale = width_scale
		self.height_scale = height_scale

	def apply(self, image: Image) -> Image:
		width = image.size[0] * self.width_scale
		height = image.size[1] * self.height_scale
		return image.resize((int(width), int(height)))

	def op_type(self) -> str:
		return "resize w/ scale"


class AspectScaleOp(ImageOp):
	def __init__(self, scale: float):
		self.scale = scale

	def apply(self, image: Image) -> Image:
		width = image.size[0] * self.scale
		height = image.size[1] * self.scale
		return image.resize((int(width), int(height)))

	def op_type(self) -> str:
		return "resize w/ scale, maintaining aspect ratio"

	
if __name__ == "__main__":
	parser = argparse.ArgumentParser(description="Resize gifs with given paths.")
	parser.add_argument("output", metavar="O", type=str, help="folder to put resized gifs in")
	parser.add_argument("paths", metavar="P", type=str, nargs="+", help="paths to gifs to resize")

	parser.add_argument("-W", "--width", type=int, help="output width in pixels")
	parser.add_argument("-H", "--height", type=int, help="output height in pixels")
	parser.add_argument("--scale_width", type=float, help="output width scale as a float")
	parser.add_argument("--scale_height", type=float, help="output height scale as a float")
	parser.add_argument("-S", "--scale", type=float, help="output scale as a float")

	args = parser.parse_args()

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

	if not all([path.split(".")[-1] == "gif" for path in args.paths]):
		parser.error("All paths must be gifs")

	if not os.path.isdir(args.output):
		parser.error("Output location must be a folder")

	if args.width and args.height:
		for path in args.paths:
			ResizeOp(args.width, args.height).edit_gif_framewise(path, args.output)
	elif args.width:
		for path in args.paths:
			AspectResizeOp(width=args.width).edit_gif_framewise(path, args.output)
	elif args.height:
		for path in args.paths:
			AspectResizeOp(height=args.height).edit_gif_framewise(path, args.output)
	elif args.scale_width:
		for path in args.paths:
			ScaleOp(args.scale_width, args.scale_height).edit_gif_framewise(path, args.output)
	elif args.scale:
		for path in args.paths:
			AspectScaleOp(args.scale).edit_gif_framewise(path, args.output)
	else:
		raise TypeError("Unknown resizing type")
