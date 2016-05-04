from bs4 import BeautifulSoup
import commands
import json


def update_patch(patch):
    """Update patch JSON.

    Parses data from the URL of the newest patch. For this all to work as
    intended, we assume that the patch note page source all share a similar
    format.
    """
    status, output = commands.getstatusoutput("curl -s " + patch)
    soup = BeautifulSoup(output, "html.parser")

    notes = {}

    body = soup.find("body")
    div = body.find_next("div", id="Items")
    newitems = div.find_next("div")
    item = newitems.find_next("ul")

    for i in output.split():
        if i.startswith("[["):
            name = i[2:][:-2].strip()
        elif i.startswith("<strong>"):
            name = i[8:][:-9].strip()
        else:
            continue
        print name
        notes[name] = []
        for change in item.find_all("li"):
            notes[name].append(change.text)

        item = newitems.find_next("ul")

        if not item:
            break

    #print json.dumps(notes)


    # body = soup.find("body")
    # div = body.find_next("div", id="Heroes")
    # heroitem = div.find_next("ul")
    #
    # for i in output.split():
    #     if not i.startswith("[["):
    #         continue
    #     name = i[2:][:-2]
    #     notes[name] = []
    #     print i
    #     for change in heroitem.find_all("li"):
    #         notes[name].append(change.text)
    #         print change.text
    #
    #     heroitem = heroitem.find_next("ul")
    #
    #     if not heroitem:
    #         div = body.find_next("div", id="Heroes")
    #         heroitem = div.find_next("ul")

    #print json.dumps(notes)


def main():
    """Hub of updates for truedota2bot."""
    update_patch("http://www.dota2.com/687")


if __name__ == "__main__":
    main()
