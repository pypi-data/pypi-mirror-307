# api/models/charging_session.py

from pydantic import BaseModel, Field
from .location import Location
from typing import Optional, Dict, List


class BaseChargingSession(BaseModel):
    provider_api_base_url: str = Field(
        ...,
        example="https://providercompany.com/api/v1",
        description="The base URL of the provider's API",
    )
    provider_account_id: str = Field(
        ..., example="client_co_23407", description="The account ID of the provider"
    )
    charging_session_id: str = Field(
        ...,
        example="65e25d9f-5400-4384-be82-cff2abcdd962",
        description="The unique identifier for the charging session",
    )
    charging_session_start_time: str = Field(
        ...,
        example="2024-06-13T12:00:00Z",
        description="The start time of the charging session",
    )
    charging_session_duration_seconds: int = Field(
        ..., example=6204, description="The duration of the charging session in seconds"
    )
    charging_session_location: Location
    charging_session_kwh_reported: float = Field(
        ..., example=50.5, description="The amount of energy reported in kWh"
    )


class FullChargingSession(BaseModel):
    provider: str = Field(
        ..., example="Tritium", description="The name of the provider"
    )
    provider_api_base_url: str = Field(
        ...,
        example="https://providercompany.com/api/v1",
        description="The base URL of the provider's API",
    )
    provider_account_id: str = Field(
        ..., example="client_co_23407", description="The account ID of the provider"
    )
    provider_charging_session_id: Optional[str] = Field(
        None,
        example="65e25d9f-5400-4384-be82-cff2abcdd962",
        description="The unique identifier for the charging session given by the provider",
    )
    charging_session_id: str = Field(
        ...,
        example="65e25d9f-5400-4384-be82-cff2abcdd962",
        description="The unique identifier for the charging session",
    )
    charging_session_start_time: str = Field(
        ...,
        example="2024-06-13T12:00:00Z",
        description="The start time of the charging session",
    )
    charging_session_end_time: str = Field(
        ...,
        example="2024-06-13T12:00:00Z",
        description="The end time of the charging session",
    )
    charging_session_duration_seconds: int = Field(
        ..., example=6204, description="The duration of the charging session in seconds"
    )
    charging_session_location: Location
    charging_session_kwh_reported: float = Field(
        ..., example=50.5, description="The amount of energy reported in kWh"
    )

    vehicle_vin: Optional[str] = Field(
        None, example="1HGBH41JXMN109186", description="Vehicle VIN"
    )
    telematics_device_hardware_id: Optional[str] = Field(
        None,
        example="GBTKS9ACEZ",
        description="Unique device ID",
    )

    telematics_device_vehicle_id: Optional[str] = Field(
        None, example=281474988412320, description="Vehicle ID"
    )

    telematics_device_name: Optional[str] = Field(
        None, example="Truck 657", description="Device name"
    )

    charging_session_vehicle_odometer_kilometers: Optional[float] = Field(
        None, example=50000, description="Vehicle odometer in kilometers"
    )

    charging_session_charge_kilowatts: Optional[float] = Field(
        None, example=120, description="Charging session power in kilowatts"
    )
    charging_session_charge_current_type: Optional[str] = Field(
        None, example="DC", description="Charging session current mode either AC or DC"
    )
    charging_session_charge_voltage: Optional[float] = Field(
        None, example=240, description="Charging session voltage in volts"
    )

    charging_session_charge_amperage: Optional[float] = Field(
        None, example=40, description="Charging session amperage in amperes"
    )

    charging_session_soc_start_percentage_coefficient: Optional[float] = Field(
        None,
        example=0.20,
        description="Charging session start state of charge percentage coefficient between 0 and 1",
    )
    charging_session_soc_end_percentage_coefficient: Optional[float] = Field(
        None,
        example=0.85,
        description="Charging session end state of charge percentage coefficient between 0 and 1",
    )

    # Change to JSON string
    additional_data: Optional[str] = Field(
        None,
        example=[
            {
                "text_example": "Any comments related to the charging session",
                "base64_example": "AxsFgtZ503wv8Tc7CBLy5w==AxsFgtZ503wv8Tc7CBLy5w==AxsFgtZ503wv8Tc7CBLy5w==AxsFgtZ503wv8Tc7CBLy5w==",
                "nested_example_fields": {"field1": "value1", "field2": "value2"},
            }
        ],
    )
