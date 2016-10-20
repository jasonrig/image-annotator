import calendar
import json
from datetime import datetime

import jwt
from flask import abort
from flask import request
from httplib2 import Http
from jwt.exceptions import DecodeError

from image_annotator import settings


def current_unix_time():
    d = datetime.utcnow()
    return calendar.timegm(d.utctimetuple())


def new_token_expiry():
    return current_unix_time() + settings.JWT_EXPIRY


def sign_token(user_id):
    payload = {
        'exp': new_token_expiry(),
        'iat': current_unix_time(),
        'sub': user_id
    }
    return "Bearer " + jwt.encode(payload, settings.JWT_SECRET).decode('utf-8')


def verify_token(token):
    try:
        return jwt.decode(token.split(" ")[-1], settings.JWT_SECRET)['sub']
    except DecodeError:
        return None


def validate_gtoken_token(access_token):
    '''Verifies that an access-token is valid and
    meant for this app.

    Returns None on fail, and an e-mail on success'''

    h = Http()
    resp, cont = h.request("https://www.googleapis.com/oauth2/v2/userinfo",
                           headers={'Host': 'www.googleapis.com',
                                    'Authorization': access_token})

    if not resp['status'] == '200':
        return None

    try:
        data = json.loads(cont)
    except TypeError:
        # Running this in Python3
        # httplib2 returns byte objects
        data = json.loads(cont.decode())

    # Ensure email verified by Google
    if not data['verified_email']:
        return None

    email = data['email']

    if settings.RESTRICT_ACCESS_BY_DOMAIN:
        domain = email.split("@")[-1]
        if domain.lower() != settings.RESTRICT_ACCESS_BY_DOMAIN.lower():
            return None

    return email


def authorized_gtoken(fn):
    """Decorator that checks that requests
    contain an id-token in the request header.
    userid will be None if the
    authentication failed, and have an id otherwise.

    Usage:
    @app.route("/")
    @authorized
    def secured_root(userid=None):
        pass
    """

    def _wrap(*args, **kwargs):
        if 'Authorization' not in request.headers:
            # Unauthorized
            print("No token in header")
            abort(401)
            return None

        userid = validate_gtoken_token(request.headers['Authorization'])
        if userid is None:
            abort(401)
            return None

        return fn(userid=userid, *args, **kwargs)

    return _wrap


def authorized(fn):
    """Decorator that checks that requests
    contain an id-token in the request header.
    userid will be None if the
    authentication failed, and have an id otherwise.

    Usage:
    @app.route("/")
    @authorized
    def secured_root(userid=None):
        pass
    """

    def _wrap(*args, **kwargs):

        if settings.FLASK_DEBUG:
            return fn(userid='test@example.com', *args, **kwargs)

        if 'Authorization' not in request.headers:
            # Unauthorized
            abort(401)
            return None

        userid = verify_token(request.headers['Authorization'])
        if userid is None:
            abort(401)
            return None

        return fn(userid=userid, *args, **kwargs)

    return _wrap

def authorized_admin(fn):
    """Decorator that checks that requests
    contain an id-token in the request header.
    userid will be None if the
    authentication failed, and have an id otherwise.

    Usage:
    @app.route("/")
    @authorized
    def secured_root(userid=None):
        pass
    """

    def _wrap(*args, **kwargs):

        if settings.FLASK_DEBUG:
            return fn(userid='test@example.com', *args, **kwargs)

        if 'Authorization' not in request.headers:
            # Unauthorized
            abort(401)
            return None

        userid = verify_token(request.headers['Authorization'])
        if userid is not settings.ADMIN_USER:
            abort(401)
            return None

        return fn(userid=userid, *args, **kwargs)

    return _wrap