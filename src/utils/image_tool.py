from io import BytesIO
import os
from PIL import Image
import settings

__author__ = 'sam'


def get_thumbnail_uri(uri):
    s = os.path.splitext(uri)
    return s[0] + '_t' + s[1]


def create_thumbnail(image, size, save_path):
    image.thumbnail(size, Image.ANTIALIAS)
    image.save(save_path)


def batch_create_thumbnail(photo_dir=settings.PHOTO_DIR):
    for photo in os.listdir(photo_dir):
        photo_file = os.path.join(photo_dir, photo)
        image = Image.open(photo_file)
        create_thumbnail(image, (500, 500), photo_file)
        create_thumbnail(image, (100, 100), get_thumbnail_uri(photo_file))




