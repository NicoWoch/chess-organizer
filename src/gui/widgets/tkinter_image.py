import logging
import os.path
import tkinter as tk
from typing import Self

from PIL import Image, ImageTk

RESOURCES_DIRECTORY = '../resources/'
TEMP_DIRECTORY = '../resources/temp/'

logger = logging.getLogger(__name__)


tkinter_images_references = {}


class TkinterImage(ImageTk.PhotoImage):
    @classmethod
    def open(cls, filename: str, size: int | tuple[int, int]) -> Self | tk.PhotoImage:
        if isinstance(size, int):
            size = (size, size)

        image_key = filename, size

        if image_key in tkinter_images_references:
            return tkinter_images_references[image_key]

        new_image = cls(filename, size)
        tkinter_images_references[image_key] = new_image
        return new_image

    def __init__(self, filename: str, size: tuple[int, int]):
        self.filename = filename
        self.size = size
        self.pillow_image = self.__get_image()

        super().__init__(self.pillow_image)

    def __get_image(self) -> Image:
        temp_path = self.__get_temp_file_path()

        if os.path.isfile(temp_path):
            return Image.open(temp_path)

        res_path = RESOURCES_DIRECTORY + self.filename

        if not os.path.isfile(res_path):
            logger.error(f'Image \'{res_path}\' not found')
            res_path = RESOURCES_DIRECTORY + 'no_image.png'
            temp_path = self.__get_temp_file_path('no_image.png')

            if not os.path.isfile(res_path):
                raise ValueError('no_image.png not found too')

        if not os.path.isdir(TEMP_DIRECTORY):
            logger.info(f'Creating directory \'{TEMP_DIRECTORY}\'')
            os.mkdir(TEMP_DIRECTORY)

        logger.info(f'Rescaling image \'{res_path}\' to size {self.size}')
        image = Image.open(res_path)
        image.thumbnail(self.size)
        image.save(temp_path)

        return image

    def __get_temp_file_path(self, filename=None) -> str:
        if filename is None:
            filename = self.filename

        *name, extension = filename.split('.')
        return TEMP_DIRECTORY + '.'.join(name) + f'_{self.size[0]}x{self.size[1]}.' + extension
