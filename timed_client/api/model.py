#!/usr/bin/env python3

"""Documentation about the module... may be multi-line"""

from datetime import datetime
from . import parser

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
