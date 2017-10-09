#!/usr/bin/env python3

"""Commandline entry points"""

import sys
import click

from timed_client import config

from .interact import login_interactive, autologin
from .render   import show_user_status


@click.group()
def main():
    pass


@main.command()
def login():
    tc = login_interactive()
    config.put('token', tc.token)
    print("Okay, you're in!")


@main.command()
def status():
    try:
        tc = autologin(nointeractive=True)
    except:
        print("Not configured, or not logged in. Run this first: ")
        print("   timed-login")
        sys.exit(1)

    show_user_status(tc.user())
