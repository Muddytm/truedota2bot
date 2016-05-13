import commands


def start():
    """Run this often via cron job to keep the bot running."""

    status, output = commands.getstatusoutput("ps")

    # Will crash if pid.pid does not exist
    with open("pid.pid") as file:
        pid = file.read()

    if pid not in output:
        status, output = commands.getstatusoutput("bash check.sh")


if __name__ == "__main__":
    start()
