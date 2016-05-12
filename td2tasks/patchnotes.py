import json


def sanitize(text):
    """Sanitize some text."""
    return text.lower().replace("\'", "").strip()


def run(comment):
    """List recent changes of hero or item based on patch_notes.json."""

    patch_list = ["6.87c", "6.87"]

    request = comment.body.strip().replace("!patchnotes", "").strip()

    with open("td2tasks/patch_notes.json") as file:
        notes = json.load(file)

    patch_number = request.split()[0].strip()

    changelog = None

    # Verify if a patch number was given and if data exists for it.
    if (patch_number in patch_list and patch_number in notes):
        request = request.replace(patch_number, "").strip()
        for patch in patch_list:
            if patch_number != patch:
                continue
            for heroitem, change in notes[patch].iteritems():
                print heroitem
                if sanitize(request) in sanitize(heroitem):
                    request = heroitem
                    break
            if (patch in notes and request in notes[patch]):
                changelog = notes[patch][request]
                break
    else:
        index = 0
        done = False
        for cur_patch in patch_list:
            if done:
                break
            for heroitem, change in notes[cur_patch].iteritems():
                if sanitize(request) in sanitize(heroitem):
                    request = heroitem
                    done = True
                    break
        print request
        if request in notes[patch_number]:
            changelog = notes[patch_number][request]

    if not changelog:
        return

    url_name = request.strip().replace(" ", "_")
    response = ("[**" + request + "**](http://dota2.gamepedia.com/"
                "" + url_name + ") (" + patch_number + "):\n\n")
    for change in changelog:
        response += ("- " + change + "\n\n")

    if response != "":
        return response
