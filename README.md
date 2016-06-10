![/u/truedota2](http://i.imgur.com/0AZujla.png)

Automated moderator bot for /r/TrueDota2.

To run, you'll need the following installed and ready to go for Python:

- PRAW (Python Reddit API Wrapper)
- YAML (AKA: pyYAML - this is used to parse config.yml)
- BeautifulSoup (to parse some web stuff)
- ImgurPython
- PIL (pip install Pillow - you may need to sudo apt-get install lipjpeg-dev and zlib1g-dev, and this http://stackoverflow.com/questions/26053982/error-setup-script-exited-with-error-command-x86-64-linux-gnu-gcc-failed-wit)

You can simply "pip install" these packages.

IMPORTANT: you'll need to setup config.yml for this to work.

Edit config_template.yml with the appropriate username, password, and subreddit data, and then save it as "config.yml".

Once you're done, just "python run.py" and you're golden!
