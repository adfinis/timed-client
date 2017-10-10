#!/usr/bin/env python3

"""Commandline entry points"""

import sys
import click
import datetime

from timed_client import config

from .interact import login_interactive, autologin
from .render   import show_user_status, show_reports, show_activities
from timed_client.api.utils import parse_date


@click.group()
def main():
    pass


@main.command()
def login():
    tc = login_interactive()
    config.put('token', tc.token)
    print("Okay, you're in!")


@main.group()
def show():
    pass


@show.command()
@click.argument('day', default=datetime.date.today())
def tracking(day):
    day = parse_date(day, fallback=datetime.date.today())
    timed = autologin()
    show_activities(timed)


@show.command()
@click.argument('day', default=datetime.date.today())
def reports(day):
    day = parse_date(day, fallback=datetime.date.today())

    timed = autologin()
    show_reports(timed, day)


@main.command()
def status():
    try:
        tc = autologin(nointeractive=True)
    except:
        print("Not configured, or not logged in. Run this first: ")
        print("   timed-login")
        sys.exit(1)

    show_user_status(tc)


@main.command()
def shell():
    """Start an interactive shell

    Requires ipython to be installed."""
    import IPython

    TIMED = autologin()

    print("You can access Timed via the global variable")
    print("TIMED. Try TIMED.user() or TIMED.activity()")

    IPython.embed()
