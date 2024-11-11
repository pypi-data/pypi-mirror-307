import json

from .base import CookieBase


class JSONCookie(CookieBase):
    def __init__(self, cookie_str: str):
        self.cookie_str = cookie_str

    def to_cookie(self):
        return json.loads(self.cookie_str)

