# truedota2bot
Automated moderator bot for /r/TrueDota2

To run, you'll need the following installed and ready to go for Python:

- PRAW (Python Reddit API Wrapper)
- YAML (AKA: pyYAML - this is used to parse config.yml)
- BeautifulSoup ("pip install beautifulsoup4" - used to parse patch notes pages for balance changes)

You can simply "pip install" these packages.

IMPORTANT: you'll need to setup config.yml for this to work.

Edit config_template.yml with the appropriate username, password, and subreddit data, and then save it as "config.yml".

Once you're done, just "python run.py" and you're golden!
