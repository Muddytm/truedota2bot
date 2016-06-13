from PIL import Image
from PIL import ImageDraw
import json
import math


def create(values):
    """Create graph."""
    im = Image.open("td2tasks/assets/templateblue4.png").convert("RGBA")  # Some sort of background
    draw = ImageDraw.Draw(im)

    if isinstance(values, dict):
        new_values = []
        for item, value in values.items():
            new_values.append(value)
        values = new_values

    for value in values:
        if value > 10:
            values = [float(x) * (10. / value) for x in values]

    angle = 360. / len(values)

    origin = (im.size[0]/2, im.size[1]/2)

    points = []

    for i in list(range(len(values))):
        cur_angle = i * angle
        width = math.cos(math.radians(cur_angle)) * float(values[i]) * 18
        height = math.sin(math.radians(cur_angle)) * float(values[i]) * 18
        points.append((origin[0] - width, origin[1] - height))

    for i in list(range(len(points))):
        if i != (len(points) - 1):
            draw.line((points[i], points[i + 1]), fill="Orange", width=5)
        else:
            draw.line((points[i], points[0]), fill="Orange", width=5)

    del draw

    return im

    #im.save("tsimage.png")
