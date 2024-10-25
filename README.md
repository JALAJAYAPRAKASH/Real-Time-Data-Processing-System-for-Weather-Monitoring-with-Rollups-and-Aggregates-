# Real-Time-Data-Processing-System-for-Weather-Monitoring-with-Rollups-and-Aggregates-

# Project Overview

This script periodically checks the current temperature for a predefined list of cities. If the temperature exceeds a specified threshold for a certain number of consecutive readings, it sends an email alert.

# Usage
Weather data for selected cities every five minutes, calculating daily summaries like average, maximum, and minimum temperatures, along with the predominant weather condition. Alerts are displayed in the console and can be configured for email notifications.

# Testing

#System Setup: Verify successful system startup and API connection using a valid key.
#Data Retrieval: Simulate API calls at intervals to fetch and parse weather data for specified locations.
#Temperature Conversion: Test the conversion of temperature values from Kelvin to user-preferred units (Celsius or Fahrenheit).
#Daily Weather Summary: Simulate multiple days of weather updates to ensure accurate daily summaries of temperature and conditions.
#Alerting Thresholds: Configure thresholds for temperature and conditions, and validate that alerts are triggered only when exceeded.
