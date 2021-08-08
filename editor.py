from PIL import Image
import os


class ImageOp:
	def apply(self, image: Image) -> Image:
		raise NotImplementedError


	def op_type(self) -> str:
		raise NotImplementedError


	def edit_gif_framewise(self, path, out_folder) -> None:
		filename = os.path.join(os.path.dirname(__file__), path)
		out_filename = os.path.join(os.path.dirname(__file__), out_folder, path)

		print("Opening {}...".format(filename))
		image = Image.open(filename)

		print("Performing {} operation (framewise)...".format(self.op_type()))
		frames = []
		while True:
			frames.append(self.apply(image))
			try:
				image.seek(image.tell() + 1)
			except EOFError:
				break

		print("Writing to {}...".format(out_filename))
		if len(frames) == 0:
			raise ValueError("Gif {} is empty".format(path))
		elif len(frames) == 1:
			frames[0].save(out_filename, palette=frames[0].getpalette())
		else:
			frames[0].save(out_filename, palette=frames[0].getpalette(), save_all=True, append_images=frames[1:])
