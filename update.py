from bs4 import BeautifulSoup
import commands


def update_patches():
    """Update patches JSON.

    Parses data from http://dota2.gamepedia.com/Game_Versions.
    """
    status, output = commands.getstatusoutput("curl -s http://dota2.gamepedia.com/Game_Versions")
    soup = BeautifulSoup(output, "html.parser")

    patches = {}

    for link in soup.find_all("a"):
        patch = str(link.get("href"))[1:]  # [1:] = Get rid of the "/"
        #print patch
        #if (len(str(patch)) < 6 and len(str(patch)) > 1 and
        #        str(patch)[1] == "."):
        #    break  # We now have the latest patch


def main():
    """Hub of updates for truedota2bot."""
    update_patches()


if __name__ == "__main__":
    main()
