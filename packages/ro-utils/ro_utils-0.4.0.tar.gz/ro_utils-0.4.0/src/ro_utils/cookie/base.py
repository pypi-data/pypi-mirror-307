from abc import ABC, abstractmethod


class CookieBase(ABC):
    @abstractmethod
    def to_cookie(self):
        pass

