import json


def sanitize(text):
    """Sanitize some text."""
    return text.lower().strip()


def run(comment):
    """Get team composition and report with what the team is strongest in."""
    request = comment.body.strip().replace("!teamsummary", "").strip()

    while request.endswith(","):
        request = request[:-1].strip()

    with open("td2tasks/heroes.json") as file:
        data = json.load(file)

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

    # User has listed heroes and not a Dotabuff/YASP URL
    if "," in request:
        heroes = request.split(",")

        for hero in heroes:
            for heroname, herodata in data.iteritems():
                if sanitize(heroname).startswith(sanitize(hero)):
                    for role, rating in herodata.iteritems():
                        if role in team_data:
                            team_data[role] += rating
    else:
        return

    response = ""

    for role, rating in team_data.iteritems():
        response += ("" + role + ": **" + str(rating) + "**\n\n")

    return response
