from bs4 import BeautifulSoup
import commands

def run(submission):
    """Flair the post with the current Dota 2 patch.
    Data collected from http://dota2.gamepedia.com/Game_Versions.
    """

    # This script will read from a JSON that is updated daily from the
    # aforementioned web page. The JSON will include the patch name as well as
    # the date that it went live, and will use datetime objects to appropriately
    # assign flair to posts.

    #submission.set_flair(patch)
