from PIL import Image
import os


class ImageOp:
	def apply(self, image: Image) -> Image:
		raise NotImplementedError

	def op_type(self) -> str:
		raise NotImplementedError

	def get_frames(self, image) -> list:
		frames = []
		while True:
			frames.append(image.copy())
			try:
				image.seek(image.tell() + 1)
			except EOFError:
				break

		return frames

	def edit_gif_framewise(self, path, out_folder) -> None:
		filename = os.path.join(os.path.dirname(__file__), path)
		out_filename = os.path.join(os.path.dirname(__file__), out_folder, path)

		print("Opening {}...".format(filename))
		image = Image.open(filename)

		print("Performing {} operation (framewise)...".format(self.op_type()))
		frames = [self.apply(frame) for frame in self.get_frames(image)]
		
		if len(frames) == 0:
			raise ValueError("Gif {} is empty".format(path))

		print("Writing to {}...".format(out_filename))
		if len(frames) == 1:
			frames[0].save(out_filename, palette=frames[0].getpalette())
		else:
			frames[0].save(out_filename, palette=frames[0].getpalette(), save_all=True, append_images=frames[1:])


	def edit_gif_initial(self, path, out_folder) -> None:
		filename = os.path.join(os.path.dirname(__file__), path)
		out_filename = os.path.join(os.path.dirname(__file__), out_folder, os.path.basename(filename))

		print("Opening {}...".format(filename))
		image = Image.open(filename)
		frames = self.get_frames(image)

		if len(frames) == 0:
			raise ValueError("Gif {} is empty".format(path))

		print("Performing {} operation (initial)...".format(self.op_type()))
		print(frames[0].getpalette()[:12])
		frames[0] = self.apply(frames[0])
		print(frames[0].getpalette()[:12])

		print("Writing to {}...".format(out_filename))
		if len(frames) == 1:
			frames[0].save(out_filename, palette=frames[0].getpalette())
		else:
			frames[0].save(out_filename, palette=frames[0].getpalette(), save_all=True, append_images=frames[1:])
