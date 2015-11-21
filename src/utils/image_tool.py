from io import BytesIO
import os
from PIL import Image
import re
import settings

__author__ = 'sam'


def get_thumbnail_uri(uri):
    s = os.path.splitext(uri)
    return s[0] + '_t' + s[1]


def create_thumbnail(image, size, save_path):
    image.thumbnail(size, Image.ANTIALIAS)
    image.save(save_path)


def resize_photo(image, size, save_path):
    image.resize(size, Image.ANTIALIAS)
    image.save(save_path)


def batch_create_thumbnail(size_list, photo_dir=settings.PHOTO_DIR, filter_name=''):
    for photo in os.listdir(photo_dir):
        if filter_name and not re.match(filter_name, photo):
            continue
        photo_file = os.path.join(photo_dir, photo)
        image = Image.open(photo_file)
        for size in size_list:
            create_thumbnail(image, size, get_thumbnail_uri(photo_file))


def batch_normalized_photo(size_list, photo_dir=settings.PHOTO_DIR, filter_name=''):
    for photo in os.listdir(photo_dir):
        if filter_name and not re.match(filter_name, photo):
            continue
        photo_file = os.path.join(photo_dir, photo)
        image = Image.open(photo_file)
        for size in size_list:
            resize_photo(image, size, photo_file)





