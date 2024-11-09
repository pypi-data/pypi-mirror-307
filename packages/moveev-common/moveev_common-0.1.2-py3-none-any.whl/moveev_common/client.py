from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from . import Base
from typing import TYPE_CHECKING


class Client(Base):
    __tablename__ = "clients"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    token = Column(String, unique=True)

    services = relationship("ClientService", back_populates="client")
    credentials = relationship("Credential", back_populates="client")


from .credential import Credential
from .client_service import ClientService
