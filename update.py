# This is basically unused for TD2bot, but it's a nice experiment with
# webpage-scraping via the BeautifulSoup module.

from bs4 import BeautifulSoup
import commands
import json


def name_cleaner(name):
    """Returns nicer name than the one given ("blade_mail" -> "Blade Mail").

    Also accounts for weird alt names ("cyclone" -> "Eul's Scepter").
    """

    # We start with a bunch of exceptions that we can't solve programatically
    if name == "basher":
        return "Skull Basher"  # As opposed to the infamous "Kneecap Basher"
    elif name == "armlet":
        return "Armlet of Mordiggian"
    elif name == "ancient_janggo":  # WutFace
        return "Drums of Endurance"
    elif name == "cyclone":
        return "Eul\'s Scepter of Divinity"
    elif name == "gem":
        return "Gem of True Sight"
    elif name == "ghost":
        return "Ghost Scepter"
    elif name == "heart":
        return "Heart of Tarrasque"
    elif name == "heavens_halberd":
        return "Heaven\'s Halberd"  # This is fine, but I want an apostrophe :D
    elif name == "sphere":
        return "Linken\'s Sphere"
    elif name == "ward_observer":
        return "Observer Ward"
    elif name == "pers":  # Someone trying to be "totes hip" at Valve
        return "Perseverence"
    elif name == "pipe":
        return "Pipe of Insight"
    elif name == "refresher":
        return "Refresher Orb"
    elif name == "tpscroll":
        return "Town Portal Scroll"
    elif name == "vladmir":  # TIL it's actually "Vladmir", not "Vladimir"
        return "Vladmir\'s Offering"
    elif name == "rattletrap":
        return "Clockwerk"
    elif name == "life_stealer":
        return "Lifestealer"
    elif name == "magnataur":
        return "Magnus"
    elif name == "furion":
        return "Nature\'s Prophet"
    elif name == "necrolyte":
        return "Necrophos"
    elif name == "obsidian_destroyer":
        return "Outworld Devourer"
    elif name == "queenofpain":
        return "Queen of Pain"
    elif name == "nevermore":
        return "Shadow Fiend"
    elif name == "shredder":
        return "Timbersaw"
    elif name == "treant":
        return "Treant Protector"
    elif name == "vengefulspirit":
        return "Vengeful Spirit"
    elif name == "skeleton_king":
        return "Wraith King"  # RIP
    elif name == "zuus":  # ???
        return "Zeus"

    # "_" replaced with whitespace
    name = name.replace("_", " ")

    new_name = ""

    # Go through every word in hero/item name and capitalize properly
    for word in name.split():
        if (not word[0].isupper() and word != "of" and word != "and" and
                word != "the"):
            word = word[0].upper() + word[1:]
        new_name += word + " "

    name = new_name.strip()

    return name


def text_cleaner(text):
    """Cleans up text; escape characters, etc. will be removed.

    Pretty inefficient but it gets the job done."""

    dirty = True

    # Clean thoroughly by cleaning again if anything dirty is found.
    while dirty:
        dirty = False
        if "\n" in text:
            text = text.replace("\n", ". ")
            dirty = True
        if "\t" in text:
            text = text.replace("\t", "")
            dirty = True
        if "\r" in text:
            text = text.replace("\r", "")
            dirty = True
        if ".. " in text:
            text = text.replace(".. ", ". ")
            dirty = True
        if " . " in text:
            text = text.replace(" . ", "")
            dirty = True
        if ":. " in text:
            text = text.replace(":. ", ": ")
            dirty = True
        if "., " in text:
            text = text.replace("., ", ", ")
            dirty = True

        for index, char in enumerate(text):
            if (char == "." and index < (len(text) - 1)):
                if text[index + 1].isalpha():
                    text = list(text)
                    text.insert(index + 1, " ")
                    text = "".join(text)

    return text.strip()


def update_patch(patch):
    """Update patch JSON.

    Parses data from the URL of the newest patch. For this all to work as
    intended, we assume that the patch note page source all share a similar
    format.
    """
    status, output = commands.getstatusoutput("curl -s " + patch)
    soup = BeautifulSoup(output, "html.parser")

    notes = {}

    # I'm bad with BeautifulSoup, don't make fun of me please ._.
    body = soup.find("body")
    if (output.find("id=\"Items\"") < output.find("id=\"Heroes\"")):
        div = body.find_next("div", id="Items")
    else:
        div = body.find_next("div", id="Heroes")
    newitems = div.find_next("div")
    heroitem = newitems.find_next("ul")

    for index, i in enumerate(output.split()):
        # Hero/item names start with this
        if i.startswith("[["):
            name = i[2:][:-2].strip()
        # Except new items, which start with this. No idea why. 4Head
        elif i.startswith("<strong>"):
            if not i.endswith("</strong>"):
                nexti = output.split()[index + 1]
                # This allows for a maximum of 3 words in item or hero name
                if not nexti.endswith("</strong>"):
                    name = i[8:].strip() + " " + output.split()[index + 1] + " " + output.split()[index + 2][:-9].strip()
                else:
                    name = i[8:].strip() + " " + output.split()[index + 1][:-9].strip()
            else:
                name = i[8:][:-9].strip()
        else:
            continue
        name = name_cleaner(name)
        notes[name] = []
        # Get the changes for hero/item and format it before adding to json.
        for change in heroitem.find_all("li"):
            text = text_cleaner(change.text)
            notes[name].append(text)
            # BELOW: code that "sorta" gets subdetails. Buggy, but it exists
            # no_detail = True
            # for details in change.find_all("div"):
            #     no_detail = False
            #     for subdetails in details.find_all("p"):
            #         text = text_cleaner(subdetails.text)
            #         notes[name].append(text)
            #
            # if no_detail:
            #     text = text_cleaner(change.text)
            #     notes[name].append(text)

        # Get next hero or item
        heroitem = heroitem.find_next("ul")

        # We've gotten everything we can get
        if not heroitem:
            break

    with open("td2tasks/new_patch_notes.json", "w+") as file:
        json.dump(notes, file)


def main():
    """Hub of updates for truedota2bot."""
    #print ("Running this will override patch_notes.json. Careful what you wish "
    #       "for.")
    update_patch("https://www.dota2.com/balanceofpower")  # Supported: 6.87, 6.85


if __name__ == "__main__":
    main()
