from PIL import Image
from PIL import ImageDraw
import json

im = Image.open("teamsummary.png")  # Some sort of background
draw = ImageDraw.Draw(im)

with open("heroes_imo.json") as file:
    hero_data = json.load(file)

heroes = ["Anti-Mage", "Crystal Maiden", "Shadow Shaman", "Arc Warden",
          "Tidehunter"]
colors = ["blue", "red", "green", "purple", "orange"]
roles = ["nuker", "jungler", "carry", "disabler", "support", "escape", "pusher",
         "durable", "initiator"]

origin = (im.size[0]/2, im.size[1]/2)

role_index = 0
hero_index = 0

for role in roles:
    point = origin
    for hero in heroes:
        length = hero_data[hero][role]
        xpoint = point[0] - (length * 12)
        ypoint = point[1] - ((0.88 * 2) * (length * 12))
        new_point = (xpoint, ypoint)
        draw.line((point, new_point), fill=colors[hero_index], width=10)
        point = new_point
        hero_index += 1
        if hero_index == 5:
            hero_index = 0
    break
    #role_index += 1
    #im = im.rotate(40)
    #draw = ImageDraw.Draw(im)

del draw

im.save("teamsummary.jpg")
