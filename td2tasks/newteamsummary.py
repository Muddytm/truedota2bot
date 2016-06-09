from bs4 import BeautifulSoup
import commands
import create_graph
from PIL import Image
from PIL import ImageDraw
import json


def sanitize(text):
    """Sanitize some text."""
    return text.lower().strip()


def better_string(text):
    """Make stuff like arc_warden into Arc Warden, etc.."""
    if text == "anti-mage":
        return "Anti-Mage"
    elif text == "natures-prophet":
        return "Nature\'s Prophet"

    text = text.replace("-", " ")
    words = text.split()

    name = ""
    for word in words:
        if (word != "of" and word != "the"):
            name += (word[0].upper() + word[1:].lower() + " ")

    return name.strip()


def construct_response(heroes):
    """Construct the response that TrueDota2Bot will return."""

    team_data = {}
    team_data["carry"] = 0
    team_data["nuker"] = 0
    team_data["initiator"] = 0
    team_data["disabler"] = 0
    team_data["durable"] = 0
    team_data["escape"] = 0
    team_data["support"] = 0
    team_data["pusher"] = 0
    team_data["jungler"] = 0

    names = []

    with open("td2tasks/heroes_imo.json") as file:
        hero_data = json.load(file)

    for hero in heroes:
        for heroname, herodata in hero_data.iteritems():
            if sanitize(heroname).startswith(sanitize(hero)):
                names.append(sanitize(heroname))
                for role, rating in herodata.iteritems():
                    if role in team_data:
                        team_data[role] += rating

    return team_data, names


def run(comment):
    """Get team composition and report with what the team is strongest in."""
    request = comment.body.strip().split("!newteamsummary")[1].strip()

    while request.endswith(","):
        request = request[:-1].strip()

    # User has listed heroes and not a Dotabuff URL
    response = ""
    if "," in request:
        heroes = request.split(",")

        if len(heroes) > 5:
            return

        new_team_data, names = construct_response(heroes)

        print new_team_data
        im = create_graph.create(new_team_data)

        print names

        for name in names:
            icon = Image.open("td2tasks/assets/hero_icons/" + name.replace(" ", "_") + "_icon.png").convert("RGBA")
            offset = ((names.index(name) * 80) + 50, 15)
            im.paste(icon, offset, icon)
            names[names.index(name)] = None  # To allow for silly 5 Io teams

        im.save("tsimage.png")
