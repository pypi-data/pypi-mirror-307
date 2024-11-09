from sqlalchemy import (
    Column,
    Integer,
    DateTime,
    String,
    BigInteger,
    ForeignKey,
    UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import insert
from typing import List, Dict
from datetime import datetime
import logging
from . import Base
from sqlalchemy.dialects.postgresql import JSONB

# Create a null logger as a fallback
logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


class Vehicle(Base):
    __tablename__ = "vehicles"

    id = Column(Integer, primary_key=True)
    credential_id = Column(Integer, ForeignKey("credentials.id"), nullable=False)
    vehicle_vin = Column(String, nullable=False)
    telematics_device_vehicle_id = Column(String)
    telematics_device_hardware_id = Column(String)
    telematics_device_name = Column(String)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)
    additional_data = Column(JSONB, nullable=True)
    provider = Column(String, nullable=True)

    __table_args__ = (
        UniqueConstraint("provider", "vehicle_vin", name="uix_provider_vin"),
    )


def save_vehicles_to_db(
    credential_id: int, vehicles: List[Dict], db_session, custom_logger: None
):

    new_vehicles_count = 0
    ignored_vehicles_count = 0
    try:
        for vehicle_data in vehicles:
            vin = vehicle_data["externalIds"]["samsara.vin"]
            vehicle = {
                "credential_id": credential_id,
                "vehicle_vin": vin,
                "telematics_device_vehicle_id": vehicle_data["id"],
                "telematics_device_hardware_id": vehicle_data["externalIds"][
                    "samsara.serial"
                ],
                "telematics_device_name": vehicle_data["name"],
                "created_at": datetime.utcnow().isoformat() + "Z",
                "updated_at": datetime.utcnow().isoformat() + "Z",
            }

            stmt = insert(Vehicle).values(vehicle)
            stmt = stmt.on_conflict_do_nothing(index_elements=["vehicle_vin"])
            result = db_session.execute(stmt)

            if result.rowcount > 0:
                new_vehicles_count += 1
                logger.info(f"Vehicle saved: VIN {vin}")
            else:
                ignored_vehicles_count += 1

        db_session.commit()

        logger.info(f"Total vehicles processed: {len(vehicles)}")
        logger.info(f"New vehicles saved: {new_vehicles_count}")
        logger.info(f"Vehicles ignored (duplicates): {ignored_vehicles_count}")

    except Exception as e:
        db_session.rollback()
        logger.error(f"An error occurred while saving vehicles: {e}")
    finally:
        db_session.close()

    return new_vehicles_count
