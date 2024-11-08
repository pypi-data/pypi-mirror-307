from abc import ABC, abstractmethod
from typing import Self

from sqlalchemy.orm import Session

from ultra_framework.mixins.session_mixin import SessionMixin


class BaseRepositoryFactory(ABC, SessionMixin):

    @classmethod
    @abstractmethod
    def create_factory(cls, session: Session) -> Self: ...
