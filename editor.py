from PIL import Image
from PIL.Image import Image as Image_Type
import os
from typing import Iterator


class ImageOp:
	def get_edited_frames(self, frames: Iterator[Image_Type]) -> Iterator[Image_Type]:
		raise NotImplementedError

	def op_type(self) -> str:
		raise NotImplementedError

	def get_frames(self, image: Image_Type) -> Iterator[Image_Type]:
		while True:
			yield image.copy()
			try:
				image.seek(image.tell() + 1)
			except EOFError:
				break

	def edit_gif(self, path: str, out_folder: str) -> None:
		filename = os.path.join(os.path.dirname(__file__), path)
		out_filename = os.path.join(os.path.dirname(__file__), out_folder, os.path.basename(filename))

		print("Opening {}...".format(filename))
		image = Image.open(filename)

		print("Performing {} operation...".format(self.op_type()))
		frames = list(self.get_edited_frames(self.get_frames(image)))
		
		if len(frames) == 0:
			raise ValueError("Gif {} is empty".format(path))

		print("Writing to {}...".format(out_filename))
		if len(frames) == 1:
			frames[0].save(out_filename, palette=frames[0].getpalette())
		else:
			frames[0].save(out_filename, palette=frames[0].getpalette(), save_all=True, append_images=frames[1:])
