"""
Helper Functions Module
Utility functions for data processing and calculations.

This module demonstrates:
- Utility function organization
- Mathematical calculations
- Data formatting
- Helper functions for the dashboard
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import json

def format_currency(amount, include_cents=True):
    """
    Format a number as currency.
    
    Args:
        amount (float): Amount to format
        include_cents (bool): Whether to include cents
    
    Returns:
        str: Formatted currency string
    """
    if include_cents:
        return f"${amount:,.2f}"
    else:
        return f"${amount:,.0f}"

def format_energy(kwh, unit="kWh"):
    """
    Format energy consumption with appropriate units.
    
    Args:
        kwh (float): Energy amount in kWh
        unit (str): Unit to display
    
    Returns:
        str: Formatted energy string
    """
    return f"{kwh:,.1f} {unit}"

def calculate_carbon_footprint(kwh, emission_factor=0.92):
    """
    Calculate CO2 emissions from energy consumption.
    
    Args:
        kwh (float): Energy consumption in kWh
        emission_factor (float): lbs CO2 per kWh (default US average)
    
    Returns:
        float: CO2 emissions in pounds
    """
    return kwh * emission_factor

def get_efficiency_rating(consumption, baseline):
    """
    Calculate efficiency rating based on consumption vs baseline.
    
    Args:
        consumption (float): Current consumption
        baseline (float): Baseline/average consumption
    
    Returns:
        dict: Rating information
    """
    ratio = consumption / baseline if baseline > 0 else 1
    
    if ratio <= 0.7:
        return {'rating': 'Excellent', 'score': 95, 'color': '#28a745'}
    elif ratio <= 0.85:
        return {'rating': 'Good', 'score': 85, 'color': '#20c997'}
    elif ratio <= 1.0:
        return {'rating': 'Average', 'score': 75, 'color': '#ffc107'}
    elif ratio <= 1.2:
        return {'rating': 'Below Average', 'score': 60, 'color': '#fd7e14'}
    else:
        return {'rating': 'Poor', 'score': 40, 'color': '#dc3545'}

def calculate_savings_potential(current_usage, efficient_usage_target=0.8):
    """
    Calculate potential savings by improving efficiency.
    
    Args:
        current_usage (float): Current energy usage
        efficient_usage_target (float): Target efficiency multiplier
    
    Returns:
        dict: Savings potential information
    """
    target_usage = current_usage * efficient_usage_target
    potential_savings_kwh = current_usage - target_usage
    potential_savings_cost = potential_savings_kwh * 0.12  # $0.12 per kWh
    percentage_savings = (potential_savings_kwh / current_usage) * 100
    
    return {
        'savings_kwh': potential_savings_kwh,
        'savings_cost': potential_savings_cost,
        'percentage': percentage_savings,
        'target_usage': target_usage
    }

def get_peak_hours():
    """
    Get typical peak hours for energy usage.
    
    Returns:
        dict: Peak hour information
    """
    return {
        'morning_peak': {'start': 7, 'end': 9, 'description': 'Morning Rush'},
        'evening_peak': {'start': 17, 'end': 21, 'description': 'Evening Peak'},
        'off_peak': [
            {'start': 22, 'end': 6, 'description': 'Overnight'},
            {'start': 9, 'end': 17, 'description': 'Daytime'}
        ]
    }

def calculate_time_of_use_savings(hourly_data, peak_rate=0.18, off_peak_rate=0.08):
    """
    Calculate potential savings with time-of-use electricity rates.
    
    Args:
        hourly_data (pd.DataFrame): Hourly consumption data
        peak_rate (float): Peak hour rate per kWh
        off_peak_rate (float): Off-peak rate per kWh
    
    Returns:
        dict: Time-of-use analysis
    """
    peak_hours = get_peak_hours()
    
    # Categorize hours
    hourly_data = hourly_data.copy()
    hourly_data['rate_category'] = 'off_peak'
    
    # Mark peak hours
    morning_peak = range(peak_hours['morning_peak']['start'], peak_hours['morning_peak']['end'] + 1)
    evening_peak = range(peak_hours['evening_peak']['start'], peak_hours['evening_peak']['end'] + 1)
    
    hourly_data.loc[hourly_data['hour'].isin(morning_peak), 'rate_category'] = 'peak'
    hourly_data.loc[hourly_data['hour'].isin(evening_peak), 'rate_category'] = 'peak'
    
    # Calculate costs
    hourly_data['flat_rate_cost'] = hourly_data['consumption'] * 0.12  # Standard rate
    hourly_data['tou_cost'] = hourly_data.apply(
        lambda row: row['consumption'] * (peak_rate if row['rate_category'] == 'peak' else off_peak_rate),
        axis=1
    )
    
    flat_rate_total = hourly_data['flat_rate_cost'].sum()
    tou_total = hourly_data['tou_cost'].sum()
    savings = flat_rate_total - tou_total
    
    return {
        'flat_rate_cost': flat_rate_total,
        'tou_cost': tou_total,
        'savings': savings,
        'savings_percentage': (savings / flat_rate_total) * 100 if flat_rate_total > 0 else 0,
        'peak_usage': hourly_data[hourly_data['rate_category'] == 'peak']['consumption'].sum(),
        'off_peak_usage': hourly_data[hourly_data['rate_category'] == 'off_peak']['consumption'].sum()
    }

def generate_usage_summary(energy_data):
    """
    Generate a comprehensive usage summary.
    
    Args:
        energy_data (pd.DataFrame): Energy consumption data
    
    Returns:
        dict: Usage summary statistics
    """
    total_consumption = energy_data['consumption'].sum()
    avg_daily = energy_data['consumption'].mean()
    peak_day = energy_data.loc[energy_data['consumption'].idxmax()]
    low_day = energy_data.loc[energy_data['consumption'].idxmin()]
    
    # Calculate trends
    if len(energy_data) >= 7:
        recent_avg = energy_data['consumption'].tail(7).mean()
        older_avg = energy_data['consumption'].head(7).mean()
        trend = 'increasing' if recent_avg > older_avg else 'decreasing'
        trend_percentage = abs((recent_avg - older_avg) / older_avg) * 100
    else:
        trend = 'insufficient_data'
        trend_percentage = 0
    
    # Variability
    std_dev = energy_data['consumption'].std()
    variability = 'high' if std_dev > avg_daily * 0.3 else 'low'
    
    return {
        'total_consumption': total_consumption,
        'average_daily': avg_daily,
        'peak_day': {
            'date': peak_day['date'],
            'consumption': peak_day['consumption']
        },
        'low_day': {
            'date': low_day['date'], 
            'consumption': low_day['consumption']
        },
        'trend': trend,
        'trend_percentage': trend_percentage,
        'variability': variability,
        'standard_deviation': std_dev
    }

def load_config(config_file='config.json'):
    """
    Load configuration from JSON file.
    
    Args:
        config_file (str): Path to configuration file
    
    Returns:
        dict: Configuration dictionary
    """
    try:
        with open(config_file, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        # Return default configuration
        return {
            'energy_rates': {
                'standard': 0.12,
                'peak': 0.18,
                'off_peak': 0.08
            },
            'carbon_emission_factor': 0.92,
            'house_types': [
                'Small Apartment',
                'Medium House', 
                'Large House',
                'Mansion'
            ],
            'energy_sources': [
                'Grid Electricity',
                'Solar + Grid',
                'Solar Only',
                'Wind + Grid'
            ]
        }

def save_config(config_data, config_file='config.json'):
    """
    Save configuration to JSON file.
    
    Args:
        config_data (dict): Configuration data
        config_file (str): Path to configuration file
    """
    with open(config_file, 'w') as f:
        json.dump(config_data, f, indent=2)

def validate_data(data, required_columns):
    """
    Validate that DataFrame has required columns.
    
    Args:
        data (pd.DataFrame): Data to validate
        required_columns (list): List of required column names
    
    Returns:
        bool: True if valid, False otherwise
    """
    if not isinstance(data, pd.DataFrame):
        return False
    
    missing_columns = set(required_columns) - set(data.columns)
    return len(missing_columns) == 0

def clean_energy_data(data):
    """
    Clean and validate energy consumption data.
    
    Args:
        data (pd.DataFrame): Raw energy data
    
    Returns:
        pd.DataFrame: Cleaned energy data
    """
    data = data.copy()
    
    # Remove negative values
    data = data[data['consumption'] >= 0]
    
    # Remove extreme outliers (more than 5 standard deviations)
    mean_consumption = data['consumption'].mean()
    std_consumption = data['consumption'].std()
    upper_limit = mean_consumption + (5 * std_consumption)
    data = data[data['consumption'] <= upper_limit]
    
    # Sort by date
    if 'date' in data.columns:
        data = data.sort_values('date')
    
    return data

def interpolate_missing_data(data, method='linear'):
    """
    Interpolate missing values in energy data.
    
    Args:
        data (pd.DataFrame): Data with potential missing values
        method (str): Interpolation method
    
    Returns:
        pd.DataFrame: Data with interpolated values
    """
    data = data.copy()
    
    if 'consumption' in data.columns:
        data['consumption'] = data['consumption'].interpolate(method=method)
    
    return data

def get_comparison_metrics(current_data, baseline_data):
    """
    Compare current usage against baseline.
    
    Args:
        current_data (pd.DataFrame): Current period data
        baseline_data (pd.DataFrame): Baseline period data
    
    Returns:
        dict: Comparison metrics
    """
    current_avg = current_data['consumption'].mean()
    baseline_avg = baseline_data['consumption'].mean()
    
    difference = current_avg - baseline_avg
    percentage_change = (difference / baseline_avg) * 100 if baseline_avg > 0 else 0
    
    return {
        'current_average': current_avg,
        'baseline_average': baseline_avg,
        'difference': difference,
        'percentage_change': percentage_change,
        'improvement': difference < 0
    }
