from .base import CookieBase
from . import parse_cookie_str


class TextCookie(CookieBase):
    def __init__(self, cookie_str: str):
        self.cookie_str = cookie_str

    def to_cookie(self):
        return parse_cookie_str(self.cookie_str)

