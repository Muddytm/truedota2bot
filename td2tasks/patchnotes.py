import json


def run(comment):
    """List recent changes of hero or item based on patch_notes.json."""

    request = comment.body.strip().replace("!patchnotes", "").strip()

    with open("td2tasks/patch_notes.json") as file:
        notes = json.load(file)

    response = ""

    for name, age in notes.iteritems():
        if name.lower().startswith(request.lower()):
            response += ("**" + name + ":**\n\n")
            for change in notes[name]:
                response += ("- " + change + "\n\n")
            break

    if response != "":
        comment.reply(response)
