import os

from django.utils.text import slugify
from PIL import Image, ImageFont


def text_to_image(text):
    font_size = 36
    font_filepath = f"{os.path.dirname(__file__)}/../../static/fonts/CookieCrisp-L36ly.ttf"
    color = (67, 33, 116, 155)

    font = ImageFont.truetype(font_filepath, size=font_size)
    mask_image = font.getmask(text, "L")
    img = Image.new("RGBA", mask_image.size)
    img.im.paste(color, (0, 0) + mask_image.size, mask_image)

    img.save(f"/tmp/{slugify(text)}.png")
    return img
