from PIL import Image
from PIL import ImageDraw
import json

im = Image.open("teamsummary.png")  # Some sort of background
draw = ImageDraw.Draw(im)

with open("heroes.json") as file:
    hero_data = json.load(file)

heroes = ["Anti-Mage", "Bloodseeker", "Faceless Void", "Arc Warden",
          "Terrorblade"]
colors = ["blue", "red", "green", "purple", "orange"]
roles = ["carry"]

origin = (im.size[0]/2, im.size[1]/2)

point = origin

index = 0

for role in roles:
    for hero in heroes:
        length = hero_data[hero][role]
        new_point = (point[0]-(length*15), point[1])
        draw.line((point, new_point), fill=colors[index], width=10)
        point = new_point
        index += 1
        if index == 5:
            index = 0

del draw

im.save("teamsummary.jpg")
