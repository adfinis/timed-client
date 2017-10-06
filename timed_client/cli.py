#!/usr/bin/env python3

"""Commandline entry points"""

import sys
import getpass

from . import config

import timed_client.api.client as client


def read_info(prompt, key=None, secure=False):
    oldvalue = config.get(key) if key else None
    if secure:
        return getpass.getpass(prompt)
    else:
        # NOTE: input() in python 2 used to be evil! Not so in python 2
        if oldvalue:
            value = input('%s [%s]' % (prompt, oldvalue))
        else:
            value = input(prompt)
        if value.strip():
            return value
        return oldvalue

def login_interactive():
    tc = None
    while not tc:
        username  = read_info("Username: ", 'username')
        password  = read_info("Password: ", secure=True)
        timed_url = read_info("URL: ",      'timed_url')
        config.put('username', username)
        config.put('timed_url', timed_url)
        try:
            tc = client.Timed(url=timed_url, username=username, password=password)
        except client.LoginError:
            print("Login error, try again")
    return tc


def login():
    tc = login_interactive()
    config.put('token', tc.token)
    print("Okay, you're in!")


def _autologin(nointeractive=False):
    timed_url = config.get('timed_url')
    token     = config.get('token')
    try:
        return client.Timed(url=timed_url, token=token)
    except:
        if nointeractive:
            raise
        return login_interactive()


def status():
    try:
        tc = _autologin(nointeractive=True)
    except:
        print("Not configured, or not logged in. Run this first: ")
        print("   timed-login")
        sys.exit(1)

    user = tc.user()
    emp = user.current_employment()

    print("User: %s %s (id=%s)" % (user.first_name, user.last_name, user.id))
    print("      Employment: %s%% (%s per day)" % (emp.percentage, emp.worktime_per_day))
    print("      Balance:    %s" % user.worktime_balance)
