from sqlalchemy.orm import mapped_column, Mapped, relationship

from api.core.database import Model
from api.monitoring.persistence import WebsiteMonitor


class User(Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    email: Mapped[str] = mapped_column(unique=True)
    password: Mapped[bytes]
    website_monitors: Mapped[list['WebsiteMonitor']] = relationship(cascade='all, delete-orphan')

    def __repr__(self):
        return f'<User(id={self.id}, username={self.name})>'