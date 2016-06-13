import json


def sanitize(text):
    """Sanitize some text."""
    return text.lower().replace("\'", "").strip()


def run(comment):
    """List recent changes of hero or item based on patch_notes.json."""

    major_patch_list = ["6.88", "6.87", "6.86"]
    patch_list = ["6.88", "6.87d", "6.87c", "6.87b", "6.87", "6.86", "https://nicedotame.me"]

    request = comment.strip().split("!patchnotes")[1].strip()

    # Addressing the !patchnotes "hero/item" problem
    request = request.replace("\"", "")

    with open("td2tasks/patch_notes.json") as file:
        notes = json.load(file)

    try:
        patch_number = request.split()[0].strip()
    except IndexError:
        # No hero/item given
        return

    patch_numbers = []
    changelogs = []
    changelog = None

    # "Since" functionality suggested by /u/dpekkle
    # !patchnotes [hero/item] since [patch number]
    if (len(request.split()) >= 3 and
            request.split()[len(request.split()) - 2] == "since"):
        request = request.replace("since ", "").strip()

        if request.split()[len(request.split()) - 1] in patch_list:
            patch_til = request.split()[len(request.split()) - 1]
            #print (patch_til)
            request = request.replace(patch_til, "").strip()
            #print (request)
        else:
            return

        # Request = hero or item we want notes for
        # Patch_til = get notes up through this

        for patch in patch_list:
            for heroitem, change in notes[patch].items():
                if sanitize(heroitem).startswith(sanitize(request)):
                    request = heroitem
                    patch_numbers.append(patch)
                    changelogs.append(notes[patch][heroitem])
                    break
            if patch == patch_til:
                break
    elif (patch_number in patch_list):
        request = request.replace(patch_number, "").strip()

        if request == "":
            return

        for heroitem, change in notes[patch_number].items():
            if sanitize(heroitem).startswith(sanitize(request)):
                request = heroitem
                break

        if request in notes[patch_number]:
            changelog = notes[patch_number][request]
    else:
        newest_patch = major_patch_list[0]
        for patch in patch_list:
            if not patch.startswith(newest_patch):
                continue
            for heroitem, change in notes[patch].items():
                if sanitize(heroitem).startswith(sanitize(request)):
                    request = heroitem
                    patch_numbers.append(patch)
                    changelogs.append(notes[patch][heroitem])
                    break

    # Got nothing? Get outta here.
    if not changelog and len(changelogs) == 0:
        return

    url_name = request.strip().replace(" ", "_")
    if len(changelogs) > 0:
        response = ("[**" + request + "**](http://dota2.gamepedia.com/"
                    "" + url_name + "):\n\n")
        for i in range(len(patch_numbers)):  # We need to use indices
            response += ("*" + patch_numbers[i] + ":*\n\n")
            for change in changelogs[i]:
                response += ("- " + change + "\n\n")
    elif changelog:
        response = ("[**" + request + "**](http://dota2.gamepedia.com/"
                    "" + url_name + "):\n\n*" + patch_number + "*:\n\n")
        for change in changelog:
            response += ("- " + change + "\n\n")

    if response != "":
        return response
