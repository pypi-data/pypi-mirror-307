from sqlalchemy import (
    Column,
    Integer,
    BigInteger,
    DateTime,
    UniqueConstraint,
    ForeignKey,
    Numeric,
    String,
)
from typing import Optional
from sqlalchemy.orm import relationship
from datetime import datetime

from sqlalchemy.orm import Session
from sqlalchemy import select, inspect
from sqlalchemy.exc import IntegrityError, NoResultFound

# from logger_config import logger
from decimal import Decimal
from . import Base


class ChargingStat(Base):
    __tablename__ = "charging_stats"

    credential = relationship("Credential")

    id = Column(Integer, primary_key=True)
    vehicle_id = Column(Integer, nullable=False)
    credential_id = Column(Integer, ForeignKey("credentials.id"), nullable=False)
    charging_status = Column(Integer, nullable=False)
    ev_charging_energy_micro_wh = Column(BigInteger, nullable=True)
    ev_state_of_charge_milli_percent = Column(BigInteger, nullable=True)
    ev_charging_voltage_milli_volt = Column(BigInteger, nullable=True)
    ev_charging_current_milli_amp = Column(BigInteger, nullable=True)
    odometer_meters = Column(BigInteger, nullable=True)

    # We store location in a de-normalized manner for fast access
    location_lat = Column(Numeric(10, 8), nullable=True)
    location_long = Column(Numeric(11, 8), nullable=True)
    resolved_address = Column(String, nullable=True)

    time = Column(DateTime, nullable=False)

    # Adds a unique constraint to the table to prevent duplicate entries
    # Combining vehicle_id, charging_status and time
    __table_args__ = (
        UniqueConstraint(
            "vehicle_id", "charging_status", "time", name="_charging_status_time_uc"
        ),
    )

    def to_dict(self):
        return {
            "time": self.time.isoformat(),
            "credential_id": self.credential_id,
            "charging_status": self.charging_status,
            "ev_charging_energy_micro_wh": self.ev_charging_energy_micro_wh,
            "ev_state_of_charge_milli_percent": self.ev_state_of_charge_milli_percent,
            "resolved_address": self.resolved_address,
            "ev_charging_voltage_milli_volt": self.ev_charging_voltage_milli_volt,
            "ev_charging_current_milli_amp": self.ev_charging_current_milli_amp,
        }

    @staticmethod
    async def load_charging_stats_for_range(
        db: Session,
        credential_id: int,
        vehicle_id: int,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = datetime.now(),
    ):
        """
        Load charging statistics for a specified time range. (notice only keyword arguments are accepted)

        Args:
            credential_id (int): The credential ID to fetch stats for.
            vehicle_id (int): The vehicle ID to fetch stats for.
            start_time (Optional[datetime]): The start time of the range in ISO format.
                                        If None, fetches all stats up to the end_time.
            end_time ((Optional[datetime]): The end time of the range in ISO format.

        Returns:
            list: A list of ChargingStat objects within the specified time range.

        Example usage:
            # Fetch stats for a specific range
            stats = await ChargingStat.load_charging_stats_for_range(start_time="2024-02-29 21:20:28", end_time="2024-03-01 01:45:24")

            # Fetch all stats up to a specific end time
            all_stats = await ChargingStat.load_charging_stats_for_range(end_time="2024-03-01 01:45:24")
        """

        query = db.query(ChargingStat).filter(
            ChargingStat.time <= end_time,
            ChargingStat.vehicle_id == vehicle_id,
            ChargingStat.credential_id == credential_id,
        )

        if start_time is not None:
            query = query.filter(ChargingStat.time >= start_time)

        results = query.order_by(ChargingStat.time).all()

        return results

    @staticmethod
    # Upserts the vehicle stats to the database
    # It checks if a record with the same vehicle_id, charging_status, and time already exists
    # If it does, it updates the record with the new values
    # If it doesn't, it adds a new record
    # it gets the data from the vehicle_stats dictionary
    async def upsert_charging_stats(db: Session, vehicle_stats: dict, vehicle, logger):

        credential_id = vehicle.credential_id

        for stat in vehicle_stats[vehicle.telematics_device_vehicle_id]:
            for charging_stat in stat["evChargingStatus"]:
                try:
                    # Step 1: Initialize the dictionary with mandatory fields
                    charging_stat_fields = {
                        "vehicle_id": vehicle.id,
                        "charging_status": charging_stat["value"],
                        "time": datetime.fromisoformat(
                            charging_stat["time"].replace("Z", "+00:00")
                        ),
                    }

                    if "decorations" in charging_stat:
                        # Step 2: Add conditional fields
                        if "evChargingEnergyMicroWh" in charging_stat["decorations"]:
                            charging_stat_fields["ev_charging_energy_micro_wh"] = (
                                charging_stat["decorations"]["evChargingEnergyMicroWh"][
                                    "value"
                                ]
                            )
                        if "evRegeneratedEnergyMicroWh" in charging_stat["decorations"]:
                            charging_stat_fields["ev_regenerated_energy_micro_wh"] = (
                                charging_stat["decorations"][
                                    "evRegeneratedEnergyMicroWh"
                                ]["value"]
                            )
                        if (
                            "evStateOfChargeMilliPercent"
                            in charging_stat["decorations"]
                        ):
                            charging_stat_fields["ev_state_of_charge_milli_percent"] = (
                                charging_stat["decorations"][
                                    "evStateOfChargeMilliPercent"
                                ]["value"]
                            )
                        if "evChargingVoltageMilliVolt" in charging_stat["decorations"]:
                            charging_stat_fields["ev_charging_voltage_milli_volt"] = (
                                charging_stat["decorations"][
                                    "evChargingVoltageMilliVolt"
                                ]["value"]
                            )
                        if "evChargingCurrentMilliAmp" in charging_stat["decorations"]:
                            charging_stat_fields["ev_charging_current_milli_amp"] = (
                                charging_stat["decorations"][
                                    "evChargingCurrentMilliAmp"
                                ]["value"]
                            )
                        if "obdOdometerMeters" in charging_stat["decorations"]:
                            charging_stat_fields["odometer_meters"] = charging_stat[
                                "decorations"
                            ]["obdOdometerMeters"]["value"]
                        if "gps" in charging_stat["decorations"]:
                            charging_stat_fields["location_lat"] = charging_stat[
                                "decorations"
                            ]["gps"]["latitude"]
                            charging_stat_fields["location_long"] = charging_stat[
                                "decorations"
                            ]["gps"]["longitude"]
                            charging_stat_fields["resolved_address"] = charging_stat[
                                "decorations"
                            ]["gps"]["reverseGeo"]["formattedLocation"]

                    try:
                        existing_stat = db.execute(
                            select(ChargingStat).where(
                                ChargingStat.credential_id == credential_id,
                                ChargingStat.vehicle_id
                                == charging_stat_fields["vehicle_id"],
                                ChargingStat.charging_status
                                == charging_stat_fields["charging_status"],
                                ChargingStat.time == charging_stat_fields["time"],
                            )
                        ).scalar_one_or_none()

                        if existing_stat is None:
                            raise NoResultFound

                        # If the existing record has the same values, skip this charging event
                        if all(
                            getattr(existing_stat, key) == value
                            for key, value in charging_stat_fields.items()
                        ):
                            logger.info(
                                f"Skipping record for vehicle ID {charging_stat_fields['vehicle_id']} at {charging_stat_fields['time']}, no changes detected"
                            )
                            continue

                        # Use SQLAlchemy's inspection system to check changes
                        state = inspect(existing_stat)
                        modified_attrs = state.attrs

                        # Capture the initial state before updating
                        initial_state = {
                            key: getattr(existing_stat, key)
                            for key in charging_stat_fields.keys()
                        }

                        # Update the object in memory
                        for key, value in charging_stat_fields.items():
                            if key != "time":
                                setattr(existing_stat, key, value)

                        # Check changes
                        changes = {
                            key: (initial_state[key], getattr(existing_stat, key))
                            for key in charging_stat_fields.keys()
                            if modified_attrs[key].history.has_changes()
                            and has_significant_change(
                                key, initial_state[key], getattr(existing_stat, key)
                            )
                        }

                        if changes:
                            logger.info(
                                f"Updated record for vehicle ID {charging_stat_fields['vehicle_id']} at {charging_stat_fields['time']}"
                            )
                            for key, (old_value, new_value) in changes.items():
                                logger.info(
                                    f"Field: {key}, Old value: {old_value}, New value: {new_value}"
                                )
                        else:
                            logger.info(
                                f"Skipping record for vehicle ID {charging_stat_fields['vehicle_id']} at {charging_stat_fields['time']}, no significant changes detected"
                            )

                    except NoResultFound:
                        # No existing record found, safe to add the new charging event
                        charging_stat = ChargingStat(**charging_stat_fields)
                        charging_stat.credential_id = credential_id
                        db.add(charging_stat)
                        logger.info(
                            f"Charging stat added for vehicle ID {vehicle.telematics_device_vehicle_id} at {charging_stat_fields['time']}"
                        )

                    db.commit()

                    logger.debug("#######################")

                except IntegrityError as e:
                    await db.rollback()  # Rollback in case of a duplicate entry
                    logger.error(f"IntegrityError occurred: {e.orig}")


def has_significant_change(key, old_value, new_value):

    # Define a tolerance for floating-point comparisons
    TOLERANCE = 1e-8

    if isinstance(old_value, float):
        old_value = Decimal(str(old_value))
    if isinstance(new_value, float):
        new_value = Decimal(str(new_value))
    if isinstance(old_value, Decimal) and isinstance(new_value, Decimal):
        return abs(old_value - new_value) > TOLERANCE
    return old_value != new_value
