import os
from random import randrange

from PIL import Image, ImageFont
from django.utils.text import slugify

# light-gray    #bdc4cb	(189,196,203)
# black         #262121	(38,33,33)
# gray-brown    #7c6b65	(124,107,101)
# orange        #f2800a	(242,128,10)
# yellow-orange #efa94d	(239,169,77)

colors = [(124, 107, 101), (242, 128, 10), (239, 169, 77)]


def text_to_image(text):
    font_size = 36
    font_filepath = f"{os.path.dirname(__file__)}/../static/fonts/CookieCrisp-L36ly.ttf"
    color = colors[randrange(len(colors))]

    font = ImageFont.truetype(font_filepath, size=font_size)
    mask_image = font.getmask(text, "L")
    img = Image.new("RGBA", mask_image.size)
    img.im.paste(color, (0, 0) + mask_image.size, mask_image)

    img.save(f"/tmp/{slugify(text)}.png")
    return img
