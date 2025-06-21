"""
Data Generator Module
Generates realistic sample energy consumption data for the dashboard.

This module demonstrates:
- Working with dates and time series
- Creating realistic data patterns
- Using random data generation
- Pandas DataFrame operations
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
from faker import Faker

fake = Faker()

def generate_energy_data(days=30, house_type="Medium House"):
    """
    Generate realistic energy consumption data for a specified period.
    
    Args:
        days (int): Number of days to generate data for
        house_type (str): Type of house (affects base consumption)
    
    Returns:
        pandas.DataFrame: DataFrame with date and consumption columns
    """
    # Base consumption levels by house type
    base_consumption = {
        "Small Apartment": 15,
        "Medium House": 25,
        "Large House": 45,
        "Mansion": 80
    }
    
    base_kwh = base_consumption.get(house_type, 25)
    
    # Generate date range
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)
    date_range = pd.date_range(start=start_date, end=end_date, freq='D')
    
    consumption_data = []
    
    for date in date_range:
        # Base consumption with seasonal variation
        seasonal_factor = 1 + 0.3 * np.sin(2 * np.pi * date.dayofyear / 365)
        
        # Weekend vs weekday pattern
        if date.weekday() >= 5:  # Weekend
            weekend_factor = 1.2
        else:  # Weekday
            weekend_factor = 0.9
        
        # Weather simulation (temperature effects)
        temp_factor = 1 + 0.2 * np.sin(2 * np.pi * date.dayofyear / 365 + np.pi)
        
        # Random daily variation
        random_factor = random.uniform(0.8, 1.2)
        
        # Calculate daily consumption
        daily_consumption = base_kwh * seasonal_factor * weekend_factor * temp_factor * random_factor
        
        # Add some random spikes for special events
        if random.random() < 0.05:  # 5% chance of high usage day
            daily_consumption *= random.uniform(1.5, 2.0)
        
        consumption_data.append({
            'date': date,
            'consumption': round(daily_consumption, 2),
            'weekday': date.strftime('%A'),
            'month': date.strftime('%B'),
            'season': get_season(date)
        })
    
    return pd.DataFrame(consumption_data)

def generate_appliance_data(house_type="Medium House"):
    """
    Generate realistic appliance consumption data.
    
    Args:
        house_type (str): Type of house (affects appliance usage)
    
    Returns:
        pandas.DataFrame: DataFrame with appliance consumption data
    """
    # Appliance consumption patterns by house type
    appliance_patterns = {
        "Small Apartment": {
            "HVAC System": 8.5,
            "Water Heater": 3.2,
            "Refrigerator": 1.8,
            "Washer/Dryer": 1.5,
            "Lighting": 1.2,
            "Electronics": 2.1,
            "Cooking": 1.8,
            "Other": 1.0
        },
        "Medium House": {
            "HVAC System": 12.5,
            "Water Heater": 4.8,
            "Refrigerator": 2.2,
            "Washer/Dryer": 2.8,
            "Lighting": 2.5,
            "Electronics": 3.5,
            "Cooking": 2.5,
            "Other": 1.8
        },
        "Large House": {
            "HVAC System": 18.2,
            "Water Heater": 7.1,
            "Refrigerator": 3.1,
            "Washer/Dryer": 4.2,
            "Lighting": 4.8,
            "Electronics": 5.2,
            "Cooking": 3.8,
            "Pool/Spa": 3.5,
            "Other": 2.8
        },
        "Mansion": {
            "HVAC System": 28.5,
            "Water Heater": 10.2,
            "Refrigerator": 4.5,
            "Washer/Dryer": 6.8,
            "Lighting": 8.2,
            "Electronics": 7.8,
            "Cooking": 5.5,
            "Pool/Spa": 8.2,
            "Security System": 2.1,
            "Other": 4.2
        }
    }
    
    appliances = appliance_patterns.get(house_type, appliance_patterns["Medium House"])
    
    appliance_data = []
    for appliance, base_kwh in appliances.items():
        # Add some random variation
        actual_kwh = base_kwh * random.uniform(0.85, 1.15)
        
        # Calculate cost (assuming $0.12 per kWh)
        daily_cost = actual_kwh * 0.12
        monthly_cost = daily_cost * 30
        
        # Efficiency rating (simulate)
        efficiency = random.choice(['A+++', 'A++', 'A+', 'A', 'B', 'C'])
        
        appliance_data.append({
            'appliance': appliance,
            'daily_kwh': round(actual_kwh, 2),
            'daily_cost': round(daily_cost, 2),
            'monthly_cost': round(monthly_cost, 2),
            'efficiency_rating': efficiency,
            'percentage': 0  # Will be calculated after all data is collected
        })
    
    df = pd.DataFrame(appliance_data)
    
    # Calculate percentages
    total_consumption = df['daily_kwh'].sum()
    df['percentage'] = round((df['daily_kwh'] / total_consumption) * 100, 1)
    
    return df.sort_values('daily_kwh', ascending=False)

def generate_hourly_data(date=None, house_type="Medium House"):
    """
    Generate hourly consumption data for a specific day.
    
    Args:
        date (datetime): Date to generate data for (defaults to today)
        house_type (str): Type of house
    
    Returns:
        pandas.DataFrame: DataFrame with hourly consumption data
    """
    if date is None:
        date = datetime.now().date()
    
    base_consumption = {
        "Small Apartment": 0.8,
        "Medium House": 1.2,
        "Large House": 2.1,
        "Mansion": 3.5
    }
    
    base_hourly = base_consumption.get(house_type, 1.2)
    
    # Typical daily usage pattern (multipliers for each hour)
    hourly_pattern = [
        0.6, 0.5, 0.4, 0.4, 0.5, 0.7,  # 0-5 AM (low usage)
        1.2, 1.8, 1.5, 1.0, 0.8, 0.9,  # 6-11 AM (morning peak)
        1.0, 0.9, 0.8, 0.8, 1.1, 1.4,  # 12-5 PM (afternoon)
        1.8, 2.0, 1.9, 1.6, 1.2, 0.9   # 6-11 PM (evening peak)
    ]
    
    hourly_data = []
    for hour in range(24):
        # Base pattern with random variation
        consumption = base_hourly * hourly_pattern[hour] * random.uniform(0.8, 1.2)
        
        hourly_data.append({
            'hour': hour,
            'consumption': round(consumption, 3),
            'time': f"{hour:02d}:00",
            'period': get_time_period(hour)
        })
    
    return pd.DataFrame(hourly_data)

def get_season(date):
    """Get season based on date"""
    month = date.month
    if month in [12, 1, 2]:
        return "Winter"
    elif month in [3, 4, 5]:
        return "Spring"
    elif month in [6, 7, 8]:
        return "Summer"
    else:
        return "Fall"

def get_time_period(hour):
    """Get time period description"""
    if 5 <= hour < 12:
        return "Morning"
    elif 12 <= hour < 17:
        return "Afternoon"
    elif 17 <= hour < 22:
        return "Evening"
    else:
        return "Night"

def generate_weather_data(days=30):
    """
    Generate weather data that affects energy consumption.
    
    Args:
        days (int): Number of days to generate data for
    
    Returns:
        pandas.DataFrame: DataFrame with weather data
    """
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)
    date_range = pd.date_range(start=start_date, end=end_date, freq='D')
    
    weather_data = []
    for date in date_range:
        # Seasonal temperature variation
        base_temp = 70 + 25 * np.sin(2 * np.pi * date.dayofyear / 365)
        temp = base_temp + random.uniform(-10, 10)
        
        # Humidity (affects comfort and AC usage)
        humidity = random.uniform(30, 80)
        
        # Weather conditions
        conditions = random.choices(
            ['Sunny', 'Partly Cloudy', 'Cloudy', 'Rainy', 'Stormy'],
            weights=[40, 30, 20, 8, 2]
        )[0]
        
        weather_data.append({
            'date': date,
            'temperature': round(temp, 1),
            'humidity': round(humidity, 1),
            'conditions': conditions,
            'heating_degree_days': max(0, 65 - temp),
            'cooling_degree_days': max(0, temp - 75)
        })
    
    return pd.DataFrame(weather_data)
