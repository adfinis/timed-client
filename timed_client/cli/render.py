#!/usr/bin/env python3

"""Rendering output"""


def show_user_status(user):
    "Show the user's status (Employment, overtime balance, etc)"

    emp = user.current_employment()

    print("User: %s %s (id=%s)" % (user.first_name, user.last_name, user.id))
    print("      Employment: %s%% (%s per day)" % (emp.percentage, emp.worktime_per_day))
    print("      Balance:    %s" % user.worktime_balance)
