from typing import Iterator

from sqlalchemy.orm import sessionmaker, Session


class SessionFactory:

    def __init__(self, session_maker: sessionmaker):
        self.session_maker = session_maker

    def create_session(self) -> Iterator[Session]:
        session = self.session_maker()

        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()
