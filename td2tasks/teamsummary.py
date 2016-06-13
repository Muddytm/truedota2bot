from bs4 import BeautifulSoup
import subprocess
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

    with open("td2tasks/heroes_imo.json") as file:
        hero_data = json.load(file)

    for hero in heroes:
        for heroname, herodata in hero_data.items():
            if sanitize(heroname).startswith(sanitize(hero)):
                for role, rating in herodata.items():
                    if role in team_data:
                        team_data[role] += rating

    return team_data


def run(comment):
    """Get team composition and report with what the team is strongest in."""
    request = comment.strip().split("!teamsummary")[1].strip()

    while request.endswith(","):
        request = request[:-1].strip()

    # User has listed heroes and not a Dotabuff URL
    response = ""
    if "," in request:
        heroes = request.split(",")

        if len(heroes) > 5:
            return

        new_team_data = construct_response(heroes)

        for role, rating in new_team_data.items():
            response += ("" + role + ": **" + str(rating) + "**\n\n")

    elif (request.startswith("http://www.dotabuff.com/matches/") or
            request.startswith("www.dotabuff.com/matches/") or
            request.startswith("dotabuff.com/matches/")):

            output = subprocess(["curl", "-s", request])
            #status, output = commands.getstatusoutput("curl -s " + request)

            soup = BeautifulSoup(output, "html.parser")

            radi_heroes = []
            dire_heroes = []

            for hero in soup.find_all("div", {"class": "image-container image-container-hero image-container-icon"}):
                hero = str(hero.find("a"))

                hero = hero[17:hero.find("\"><img class=\"image-hero image-icon")]

                if len(radi_heroes) < 5:
                    radi_heroes.append(better_string(hero))
                elif len(dire_heroes) < 5:
                    dire_heroes.append(better_string(hero))
                else:
                    break

            radi_data = construct_response(radi_heroes)
            dire_data = construct_response(dire_heroes)

            response += ("#**Radiant:**\n\n")
            for role, rating in radi_data.items():
                response += ("" + role + ": **" + str(rating) + "**\n\n")

            response += ("\n\n#**Dire:**\n\n")
            for role, rating in dire_data.items():
                response += ("" + role + ": **" + str(rating) + "**\n\n")
    else:
        return

    return response
