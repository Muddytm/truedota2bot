![/u/truedota2](http://i.imgur.com/0AZujla.png)

Automated moderator bot for /r/TrueDota2.

This bot was initially made for the Reddit functionality (specifically for
/u/TrueDota2), but it's completely free for anyone to use for their own
subreddit, Discord server, etc.

The complete package requires the following to be installed:

- PRAW (Python Reddit API Wrapper)
- YAML (AKA: pyYAML - this is used to parse config.yml)
- BeautifulSoup (AKA bs4; to parse some web stuff)
- ImgurPython
- PIL (pip install Pillow - you may need to sudo apt-get install lipjpeg-dev and zlib1g-dev, and maybe this http://stackoverflow.com/questions/26053982/error-setup-script-exited-with-error-command-x86-64-linux-gnu-gcc-failed-wit)

NOTE: to run the Discord script, you will need Python 3.5 and Discord.py, as
posted here: https://github.com/Rapptz/discord.py

You'll need to setup config.yml for this to work on Reddit, and
config_discord.yml for Discord. It's pretty self-explanatory if you look at the
names of the variables in the template files.

Once you're done, just "python run.py" and/or "python3.5 run_discord.py" and
you're golden!
