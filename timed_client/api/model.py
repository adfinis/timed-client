#!/usr/bin/env python3

"""Documentation about the module... may be multi-line"""

from datetime import datetime, timedelta
import pytz

from . import parser
from . import utils

@parser.model_for('users')
class User(parser.APIModel):

    def current_employment(self):
        now = datetime.now()
        for emp in self.employments:
            start_date = datetime.strptime(emp.start_date, '%Y-%m-%d')
            try:
                end_date   = datetime.strptime(emp.end_date  , '%Y-%m-%d')
            except:
                end_date = datetime.now()

            if start_date < now and end_date >= now:
                return emp


@parser.model_for('activities')
class Activity(parser.APIModel):
    def current_duration(self):
        """Return duration as datetime.timedelta

        Note that this works regardless of whether we're still tracking or
        not
        """

        return sum([
            b.current_duration()
            for b in self.blocks
        ], timedelta(0))


@parser.model_for('activity-blocks')
class ActivityBlock(parser.APIModel):
    def current_duration(self):
        """Return duration as datetime.timedelta

        Note that this works regardless of whether we're still tracking or not
        """
        end   = self.get_end_time()
        start = self.get_start_time()
        diff = utils.difftime(end, start)

        return diff

    def get_start_time(self):
        return utils.parse_time(self.from_time)

    def get_end_time(self):
        if self.to_time:
            return utils.parse_time(self.to_time)
        return datetime.now().time()


@parser.model_for('reports')
class Report(parser.APIModel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.duration = utils.parse_timedelta(self.duration)
