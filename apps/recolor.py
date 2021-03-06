from PIL.Image import Image
import argparse
from editor import ImageOp
import numpy as np
from path_args import PathArgs
import cv2
from typing import Iterator


def get_palette_hsv(image: Image) -> np.array:
	palette = image.getpalette()
	colors = len(palette) // 3
	np_palette = np.array(palette, dtype=np.uint8)
	np_palette.resize((1, colors, 3))
	np_palette = cv2.cvtColor(np_palette, cv2.COLOR_RGB2HSV)
	return np_palette


def put_palette_from_hsv(image: Image, np_hsv: np.array) -> None:
	image.putpalette(cv2.cvtColor(np_hsv, cv2.COLOR_HSV2RGB).flatten())


class RecolorArgs:
	@staticmethod
	def create_args(parser: argparse.ArgumentParser) -> None:
		parser.add_argument("-H", "--hue", type=float, help="hue shift in degrees (-180 to 180)")
		parser.add_argument("--set_hue", type=float, help="set hue value in degrees (0 to 360)")

	@staticmethod
	def check_args(parser: argparse.ArgumentParser, args) -> None:
		if args.hue and args.set_hue:
			parser.error("Cannot shift hue and set hue")

		if args.hue and (args.hue < -180 or args.hue > 180):
			parser.error("Hue shift must be between -180 and 180")

		if args.set_hue and (args.set_hue < 0 or args.set_hue >= 360):
			parser.error("Hue value must be between 0 and 360")


class HueShiftOp(ImageOp):
	def __init__(self, hue_shift: float):
		self.hue_shift = hue_shift

	def get_edited_frames(self, frames: Iterator[Image]) -> Iterator[Image]:
		for image in frames:
			hsvPalette = get_palette_hsv(image).astype(np.int16)
			hsvPalette[:, :, 0] += 360 # add offset to avoid negative overflow 
			hsvPalette[:, :, 0] += int(self.hue_shift / 2) # hue is in range [0, 180)
			hsvPalette[:, :, 0] = hsvPalette[:, :, 0] % 180
			hsvPalette = hsvPalette.astype(np.uint8)
			put_palette_from_hsv(image, hsvPalette)
			yield image

	def op_type(self) -> str:
		return "hue shift"


class HueSetOp(ImageOp):
	def __init__(self, hue: float):
		self.hue = hue

	def get_edited_frames(self, frames: Iterator[Image]) -> Iterator[Image]:
		for image in frames:
			hsvPalette = get_palette_hsv(image)
			hsvPalette[:, :, 0] = int(self.hue / 2) # hue is in range [0, 180)
			put_palette_from_hsv(image, hsvPalette)
			yield image

	def op_type(self) -> str:
		return "hue set"


def make_parser() -> argparse.ArgumentParser:
	parser = argparse.ArgumentParser(description="Recolor gifs with given paths.")
	PathArgs.create_args(parser)
	RecolorArgs.create_args(parser)
	return parser

if __name__ == "__main__":
	parser = make_parser()
	args = parser.parse_args()
	PathArgs.check_args(parser, args)
	RecolorArgs.check_args(parser, args)

	if args.hue:
		for path in args.paths:
			HueShiftOp(args.hue).edit_gif(path, args.output)
	elif args.set_hue:
		for path in args.paths:
			HueSetOp(args.set_hue).edit_gif(path, args.output)
	else:
		raise TypeError("Unknown resizing type")
