__author__ = 'sam'
import os
from PIL import Image
from io import BytesIO
import random

_BASE = map(str, range(10)) + map(chr, range(65, 91))
_CODE_LEN = 5
def gen_code(size=None):
    len_base = len(_BASE)
    code = ''
    font_image = Image.open(os.path.join(os.path.dirname(__file__),'font.png'))
    code_image = Image.new('RGBA', (19 * _CODE_LEN, 25))
    for c in range(_CODE_LEN):
        rand_ci = random.randint(0, 35)
        code += _BASE[rand_ci]
        img_c = font_image.crop((rand_ci * 19, 0, (rand_ci + 1) * 19, 20))
        img_c = img_c.rotate(random.randint(-30, 30))
        code_image.paste(img_c, (c * 19, 2))
    if size:
        code_image.thumbnail(size, Image.ANTIALIAS)
    out = BytesIO()
    code_image.save(out, 'PNG')
    return code, out.getvalue()



