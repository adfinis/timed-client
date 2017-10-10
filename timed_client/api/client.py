#!/usr/bin/env python3

"""Timed API client"""
import functools
import json
import base64
import datetime
import requests
from . import parser
from . import model

class LoginError(RuntimeError): pass

class Timed:
    def __init__(self, url, **kwargs):
        """Instantiate new timed client

        To log in, pass either a 'token' parameter,
        or 'username' and 'password'."""

        self.token = None
        self.url   = url
        self._api   = ('%s/api/v1' % url).strip('/')

        if 'username' in kwargs:
            self._login(**kwargs)

        elif 'token' in kwargs:
            self.token = kwargs['token']

    def _path(self, path):
        return '%s/%s' % (self._api, path)

    def _login(self, username, password):
        params = {
            'data': {
                'type': 'obtain-json-web-tokens',
                'id': None,
                'attributes': {
                    'username': username,
                    'password': password
                }
            }
        }
        resp = requests.post(
            self._path('auth/login'),
            json=params,
            headers={'Content-Type':'application/vnd.api+json'})
        data = resp.json()
        try:
            self.token = data['data']['token']
        except KeyError:
            # Erhm, something bad
            raise LoginError("Login failed")

    @property
    @functools.lru_cache()
    def _auth_info(self):
        token_data = self.token.split('.')[1]
        padding = len(token_data) % 4
        token_data += '=' * padding

        return json.loads(base64.b64decode(token_data).decode('UTF-8'))

    @functools.lru_cache()
    def user(self):
        return self._get(
            'users/%d' % self._auth_info['user_id'],
            {'include': 'employments,employments.location'})


    def activities(self, date=None):
        """Return the (tracking) activities of the given date

        If no date is given, defaults to today. Date should
        be a python `datetime.date` object.
        """

        if date is None:
            date = datetime.date.today()

        return self._get(
            'activities',
            {
                'include': 'blocks,task,task.project,task.project.customer',
                'day': date.isoformat()
             })

    def reports(self, date=None):
        """Return the timesheet report entries of the given date

        If no date is given, defaults to today. Date should
        be a python `datetime.date` object.
        """

        if date is None:
            date = datetime.date.today()

        return self._get(
            'reports',
            {
                'include': 'task,task.project,task.project.customer',
                'date': date.isoformat(),
                'user': self.user().id
             })

    def customers(self, search=None):
        return self._get('customers')

    def _get(self, url, params={}):
        resp = self._session.get(self._path(url), params=params)
        data = resp.json()
        try:
            return parser.APIResult.from_resp(self, **data)
        except:
            raise
            raise self._error_from(data)

    def _post(self, url, data):
        return self._session.post(self._path(url), params=data).json()

    def _error_from(self, data):
        return RuntimeError(data)

    @property
    @functools.lru_cache()
    def _session(self):
        session = requests.Session()
        session.headers['Authorization'] = 'Bearer %s' % self.token

        return session
