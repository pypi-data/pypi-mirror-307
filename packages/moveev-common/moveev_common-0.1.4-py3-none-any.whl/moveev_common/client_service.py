from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from typing import TYPE_CHECKING
from . import Base


class ClientService(Base):
    __tablename__ = "client_services"

    id = Column(Integer, primary_key=True)
    client_id = Column(Integer, ForeignKey("clients.id"), nullable=False)
    service_id = Column(Integer, ForeignKey("services.id"), nullable=False)

    client = relationship("Client", back_populates="services")
    service = relationship("Service")
    event_logs = relationship("EventLog", back_populates="client_service")

    @staticmethod
    def add_client_service(client_id: int, service_id: int, db_session):

        new_client_service = ClientService(client_id=client_id, service_id=service_id)
        db_session.add(new_client_service)
        db_session.commit()
        db_session.refresh(new_client_service)
        return new_client_service


from .service import Service
from .event_log import EventLog
