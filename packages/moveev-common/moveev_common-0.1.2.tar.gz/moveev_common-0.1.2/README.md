# MoveEV Common Models

This package contains the common models used for Electric Vehicle (EV) Charging Data across the MoveEV ecosystem.

## Overview

The `moveev_common` package provides a set of standardized data models that represent various aspects of EV charging sessions, vehicle information, and location data. These models ensure consistency and interoperability between different components of the MoveEV platform.

## Models

The package includes the following main models:

1. **ChargingSession**: Represents a charging session for an electric vehicle, including details such as start time, duration, energy consumed, and location.

2. **Vehicle**: Contains information about an electric vehicle, including its VIN, telematics device details, and associated credential information.

3. **Location**: Represents geographical location data, including latitude, longitude, and resolved address information.

## Usage

These models can be imported and used in various MoveEV projects to ensure consistent data structures when working with EV charging data. They provide a common language for different components of the system to communicate and share information effectively.

## Contributing

When adding new fields or modifying existing models, please ensure that changes are reflected across all relevant components of the MoveEV ecosystem to maintain consistency.

For more detailed information about each model and its fields, please refer to the source code and inline documentation.
