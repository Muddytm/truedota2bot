import json


def sanitize(text):
    """Sanitize some text."""
    return text.lower().replace("\'", "").strip()


def run(comment):
    """List recent changes of hero or item based on patch_notes.json."""

    patch_list = ["6.87c", "6.87b", "6.87", "https://nicedotame.me"]

    request = comment.body.strip().replace("!patchnotes", "").strip()

    # Addressing the !patchnotes "hero/item" problem
    request = request.replace("\"", "")

    with open("td2tasks/patch_notes.json") as file:
        notes = json.load(file)

    try:
        patch_number = request.split()[0].strip()
    except IndexError:
        # No hero/item given
        return

    changelog = None

    # Verify if a patch number was given and if data exists for it.
    if (patch_number in patch_list):
        request = request.replace(patch_number, "").strip()

        if request == "":
            return

        for heroitem, change in notes[patch_number].iteritems():
            if sanitize(request) in sanitize(heroitem):
                request = heroitem
                break
            else:
                done = False
                for word in sanitize(request).split():
                    if (word in sanitize(heroitem) and word != "the" and
                            word != "of"):
                        request = heroitem
                        done = True
                        break
                if done:
                    break

        if request in notes[patch_number]:
            changelog = notes[patch_number][request]
    else:
        done = False
        for patch in patch_list:
            if done:
                break
            for heroitem, change in notes[patch].iteritems():
                if sanitize(request) in sanitize(heroitem):
                    patch_number = patch
                    request = heroitem
                    changelog = notes[patch][request]
                    done = True
                    break
                else:
                    for word in sanitize(request).split():
                        if (word in sanitize(heroitem) and word != "the" and
                                word != "of"):
                            patch_number = patch
                            request = heroitem
                            changelog = notes[patch][request]
                            done = True
                            break
                    if done:
                        break

    if not changelog:
        return

    url_name = request.strip().replace(" ", "_")
    response = ("[**" + request + "**](http://dota2.gamepedia.com/"
                "" + url_name + ") (" + patch_number + "):\n\n")
    for change in changelog:
        response += ("- " + change + "\n\n")

    if response != "":
        return response
