#!/usr/bin/env python3

import getpass

from timed_client import config
import timed_client.api.client as client


def read_info(prompt, key=None, secure=False):
    "Get Info from user, defaulting to key in config"
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
    "Login interactively. Ask for params before logging in"
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


def autologin(nointeractive=False):
    "Try to login automatically with stored token."
    timed_url = config.get('timed_url')
    token     = config.get('token')
    try:
        return client.Timed(url=timed_url, token=token)
    except:
        if nointeractive:
            raise
        return login_interactive()

