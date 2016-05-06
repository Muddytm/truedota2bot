import json


def run(comment):
    """List recent changes of hero or item based on patch_notes.json."""

    request = comment.body.strip().replace("!patchnotes", "").strip()

    with open("td2tasks/patch_notes.json") as file:
        notes = json.load(file)

    response = ""

    for name, age in notes.iteritems():
        if name.lower().startswith(request.lower()):
            url_name = name.strip().replace(" ", "_")
            response += ("[**" + name + "**](http://dota2.gamepedia.com/" + url_name + ") (6.87):\n\n")
            for change in notes[name]:
                response += ("- " + change + "\n\n")
            break

    if response != "":
        return response
