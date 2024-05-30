from sqlalchemy import ForeignKey
from sqlalchemy.orm import mapped_column, Mapped

from api.database import Model


class WebsiteMonitor(Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    url: Mapped[str]
    interval_minutes: Mapped[int]
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete='CASCADE'))

    def __repr__(self):
        return f'<WebsiteMonitor(id={self.id}, url={self.url})>'