from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# Import models after Base is defined
from .client import Client
from .credential import Credential
from .charging_stat import ChargingStat
from .charging_event import ChargingEvent
from .last_run_time import LastRunTime
from .client_service import ClientService
from .vehicle import Vehicle
from .service import Service
from .charging_session import FullChargingSession
from .location import Location
from .event_log import EventLog
