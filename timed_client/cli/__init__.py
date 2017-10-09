#!/usr/bin/env python3

"""Commandline entry points"""

import sys
import click

from timed_client import config

from .interact import login_interactive, autologin


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

    user = tc.user()
    emp = user.current_employment()

    print("User: %s %s (id=%s)" % (user.first_name, user.last_name, user.id))
    print("      Employment: %s%% (%s per day)" % (emp.percentage, emp.worktime_per_day))
    print("      Balance:    %s" % user.worktime_balance)

