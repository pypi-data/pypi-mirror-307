from sqlalchemy import Column, Integer, String
from . import Base


class Service(Base):
    __tablename__ = "services"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    url = Column(String, nullable=False)

    def __repr__(self):
        return f"<Service(id={self.id}, name='{self.name}', url='{self.url}')>"
