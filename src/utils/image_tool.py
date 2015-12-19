# coding: utf-8
from io import BytesIO
import os
from PIL import Image
import re
import settings

__author__ = 'sam'


def pic_info(self, img):
    '''''获取照片的尺寸'''
    w, h = img.size
    if w > h:
        return w, h, 0  # 横版照片
    else:
        return w, h, 1  # 竖版照片


def comp_num(self, x, y):
    '''''比较两个实数
    如果是用直接比较话会出现经典的整数除得0问题
    '''
    x = float(x)
    y = float(y)
    return float(x / y)

def pic_resize(self, picname, p_w, p_h):
    '''''根据设定的尺寸，对指定照片进行像素调整'''

    # 获取指定照片的规格，一般是1024,768
    img = Image.open(picname)
    w, h, isVertical = self.pic_info(img)

    # 判断照片横竖，为竖版的话对调w,h
    if isVertical:
        p_w, p_h = p_h, p_w

        # 如果照片调整比例合适，直接输出
    if self.comp_num(p_h, p_w) == self.comp_num(h, w):
        target = img.resize(
            (int(p_w), int(p_h)),
            Image.ANTIALIAS  # hack: 参数呐！高保真必备！
        )
        # ANTIALIAS: a high-quality downsampling filter
        # BILINEAR: linear interpolation in a 2x2 environment
        # BICUBIC: cubic spline interpolation in a 4x4 environment

        return target

        # 比例不合适就需要对照片进行计算，保证输出照片的正中位置
    # 算法灵感来源于ColorStrom
    if self.comp_num(p_h, p_w) > self.comp_num(h, w):
        # 240/320 > 360/576 偏高照片的处理

        # 以高为基准先调整照片大小
        p_w_n = p_h * self.comp_num(w, h)  # 根据新高按比例设置新宽
        temp_img = img.resize(
            (int(p_w_n), int(p_h)),
            Image.ANTIALIAS
        )

        # 获取中间选定大小区域
        c = (p_w_n - p_w) / 2  # 边条大小
        box = (c, 0, c + p_w, p_h)  # 选定容器
        box = tuple(map(int, box))  # 转换成crop需要的int形参数
        target = temp_img.crop(box)

        return target

    else:
        # 偏宽的照片

        # 以宽为基准先调整照片大小
        p_h_n = p_w * self.comp_num(h, w)  # 根据新宽按比例设置新高
        temp_img = img.resize(
            (int(p_w), int(p_h_n)),
            Image.ANTIALIAS
        )

        # 获取新图像
        c = (p_h_n - p_h) / 2
        box = (0, c, p_w, c + p_h)
        box = tuple(map(int, box))
        target = temp_img.crop(box)

        return target


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
