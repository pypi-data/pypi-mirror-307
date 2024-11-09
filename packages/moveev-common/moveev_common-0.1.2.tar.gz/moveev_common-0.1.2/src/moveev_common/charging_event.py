from . import Base
import hashlib
from datetime import datetime

from .charging_stat import ChargingStat
from .credential import Credential
from .vehicle import Vehicle
from decimal import Decimal


from sqlalchemy import (
    Column,
    Integer,
    DateTime,
    String,
    Numeric,
    BigInteger,
    ForeignKey,
    UniqueConstraint,
    Index,
)
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import JSONB

import logging


# Create a null logger as a fallback
logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


class ChargingEvent(Base):
    __tablename__ = "charging_events"
    __table_args__ = (
        UniqueConstraint("charging_event_id", name="uq_charging_event_id"),
        Index(
            "uq_provider_event_id_provider",
            "provider_charging_event_id",
            "provider",
            unique=True,
            postgresql_where=Column("provider_charging_event_id").isnot(None),
        ),
    )

    credentials = relationship("Credential", lazy="joined")
    vehicle = relationship("Vehicle", lazy="joined")

    id = Column(Integer, primary_key=True)
    charging_event_id = Column(String, nullable=False, unique=True, index=True)
    provider = Column(String, nullable=True)
    provider_charging_event_id = Column(String, nullable=True)
    credential_id = Column(Integer, ForeignKey("credentials.id"), nullable=False)
    vehicle_id = Column(Integer, ForeignKey("vehicles.id"), nullable=True)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=True)
    duration = Column(Integer, nullable=True)
    kwh_reported = Column(Numeric(8, 3), nullable=False)
    location_lat = Column(Numeric(10, 8), nullable=True)
    location_long = Column(Numeric(11, 8), nullable=True)
    resolved_address = Column(String, nullable=True)
    ev_charging_voltage_milli_volt = Column(BigInteger, nullable=True)
    ev_charging_current_milli_amp = Column(BigInteger, nullable=True)
    charge_kilowatts = Column(Numeric(5, 2), nullable=True)
    synced_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    event_stats_json = Column(JSONB, nullable=True)
    odometer_meters = Column(BigInteger, nullable=True)
    start_soc = Column(Numeric(5, 2), nullable=True)
    end_soc = Column(Numeric(5, 2), nullable=True)
    start_energy_micro_wh = Column(BigInteger, nullable=True)
    end_energy_micro_wh = Column(BigInteger, nullable=True)
    charge_type = Column(String, nullable=True)
    additional_data = Column(JSONB, nullable=True)

    def __init__(
        self,
        start_time,
        end_time=None,
        start_soc=None,
        end_soc=None,
        uwh_reported=None,
        kwh_reported=None,
        created_at=None,
        duration=None,
        location_lat=None,
        location_long=None,
        resolved_address=None,
        ev_charging_voltage_milli_volt=None,
        ev_charging_current_milli_amp=None,
        start_energy_micro_wh=None,
        end_energy_micro_wh=None,
        odometer_meters=None,
        charge_type=None,
        charging_event_id=None,
        provider_charging_event_id=None,
        provider=None,
        telematics_device_hardware_id=None,
        charge_kilowatts=None,
        additional_data=None,
    ):
        self.duration = duration
        self.start_time = start_time
        self.end_time = end_time
        self.start_soc = start_soc
        self.end_soc = end_soc
        self.uwh_reported = uwh_reported
        self.kwh_reported = kwh_reported
        self.location_lat = location_lat
        self.location_long = location_long
        self.resolved_address = resolved_address
        self.ev_charging_voltage_milli_volt = ev_charging_voltage_milli_volt
        self.ev_charging_current_milli_amp = ev_charging_current_milli_amp
        self.created_at = created_at or datetime.utcnow()
        self.start_energy_micro_wh = start_energy_micro_wh
        self.end_energy_micro_wh = end_energy_micro_wh
        self.odometer_meters = odometer_meters
        self.charge_type = charge_type
        self.provider_charging_event_id = provider_charging_event_id
        self.provider = provider
        self.charge_kilowatts = charge_kilowatts
        self.additional_data = additional_data
        if charging_event_id is None:
            self.charging_event_id = self.generate_charging_event_id(
                telematics_device_hardware_id
            )
        else:
            self.charging_event_id = charging_event_id

    def generate_charging_event_id(self, telematics_device_hardware_id) -> str:

        # Convert start_time and end_time to ISO format strings
        start_time_str = self.start_time.isoformat()
        end_time_str = self.end_time.isoformat() if self.end_time else ""

        hardware_id = telematics_device_hardware_id or ""

        # Combine start_time, and end_time
        combined = f"{self.provider_charging_event_id}:{hardware_id}:{start_time_str}:{end_time_str}"

        # Create SHA256 hash
        return hashlib.sha256(combined.encode()).hexdigest()

    def set_event_stats_json(self, stats):
        self.event_stats_json = [
            stat.to_dict() if isinstance(stat, ChargingStat) else stat for stat in stats
        ]

    def get_event_stats_json(self):
        return self.event_stats_json

    @staticmethod
    def convert_milli_percent_to_percent(milli_percent):
        if milli_percent is not None:
            return Decimal(milli_percent) / Decimal(1000)
        return None

    @staticmethod
    def convert_micro_wh_to_kwh(micro_wh):
        if micro_wh is not None:
            return Decimal(micro_wh) / Decimal(1_000_000_000)
        return None
