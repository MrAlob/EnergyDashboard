"""
Energy Saving Tips Module
Provides personalized energy-saving recommendations based on user data.

This module demonstrates:
- Conditional logic based on user data
- String formatting and templates
- Data-driven recommendations
- User interface components
"""

import streamlit as st
import random
from datetime import datetime

def get_energy_tips(house_type, energy_source, current_usage, avg_usage, season=None):
    """
    Generate personalized energy-saving tips based on user profile and usage.
    
    Args:
        house_type (str): Type of house
        energy_source (str): Primary energy source
        current_usage (float): Current energy usage
        avg_usage (float): Average energy usage
        season (str): Current season (optional)
    
    Returns:
        list: List of personalized energy tips
    """
    tips = []
    
    # Determine current season if not provided
    if season is None:
        month = datetime.now().month
        if month in [12, 1, 2]:
            season = "Winter"
        elif month in [3, 4, 5]:
            season = "Spring"
        elif month in [6, 7, 8]:
            season = "Summer"
        else:
            season = "Fall"
    
    # Usage-based tips
    if current_usage > avg_usage * 1.2:
        tips.extend(get_high_usage_tips(house_type, season))
    elif current_usage < avg_usage * 0.8:
        tips.extend(get_efficient_usage_tips())
    else:
        tips.extend(get_moderate_usage_tips(house_type))
    
    # House type specific tips
    tips.extend(get_house_type_tips(house_type))
    
    # Energy source specific tips
    tips.extend(get_energy_source_tips(energy_source))
    
    # Seasonal tips
    tips.extend(get_seasonal_tips(season))
    
    # General tips
    tips.extend(get_general_tips())
    
    # Remove duplicates and shuffle
    unique_tips = list({tip['title']: tip for tip in tips}.values())
    random.shuffle(unique_tips)
    
    return unique_tips[:8]  # Return top 8 tips

def get_high_usage_tips(house_type, season):
    """Tips for high energy usage households"""
    tips = [
        {
            'title': '🌡️ Optimize Your Thermostat',
            'description': 'Set your thermostat 2-3°F higher in summer and lower in winter. This can save 10-15% on your energy bill.',
            'savings': '$15-30/month',
            'difficulty': 'Easy',
            'category': 'HVAC'
        },
        {
            'title': '🔌 Unplug Phantom Loads',
            'description': 'Unplug electronics when not in use. Devices in standby mode can account for 5-10% of your electricity bill.',
            'savings': '$8-15/month',
            'difficulty': 'Easy',
            'category': 'Electronics'
        },
        {
            'title': '💡 LED Light Upgrade',
            'description': 'Replace incandescent bulbs with LED lights. LEDs use 75% less energy and last 25 times longer.',
            'savings': '$12-25/month',
            'difficulty': 'Easy',
            'category': 'Lighting'
        }
    ]
    
    if season == "Summer":
        tips.append({
            'title': '❄️ AC Maintenance',
            'description': 'Clean or replace AC filters monthly. A dirty filter makes your AC work harder and use more energy.',
            'savings': '$20-40/month',
            'difficulty': 'Easy',
            'category': 'HVAC'
        })
    elif season == "Winter":
        tips.append({
            'title': '🔥 Heating Efficiency',
            'description': 'Use ceiling fans to circulate warm air. Set fans to rotate clockwise in winter to push warm air down.',
            'savings': '$10-20/month',
            'difficulty': 'Easy',
            'category': 'HVAC'
        })
    
    return tips

def get_efficient_usage_tips():
    """Tips for already efficient households"""
    return [
        {
            'title': '⭐ You\'re Doing Great!',
            'description': 'Your energy usage is below average. Keep up the good work with these advanced optimization tips.',
            'savings': 'Continued savings',
            'difficulty': 'Easy',
            'category': 'Motivation'
        },
        {
            'title': '🏠 Smart Home Upgrade',
            'description': 'Consider smart thermostats and energy monitors to optimize your already efficient usage patterns.',
            'savings': '$5-15/month',
            'difficulty': 'Moderate',
            'category': 'Technology'
        },
        {
            'title': '☀️ Solar Panel Consideration',
            'description': 'With your low usage, solar panels could make you energy independent and potentially earn money.',
            'savings': '$50-100/month',
            'difficulty': 'Hard',
            'category': 'Renewable'
        }
    ]

def get_moderate_usage_tips(house_type):
    """Tips for moderate energy usage households"""
    tips = [
        {
            'title': '🌊 Water Heater Optimization',
            'description': 'Lower your water heater temperature to 120°F and insulate the tank and pipes.',
            'savings': '$10-25/month',
            'difficulty': 'Easy',
            'category': 'Water Heating'
        },
        {
            'title': '🪟 Seal Air Leaks',
            'description': 'Use caulk and weatherstripping to seal air leaks around windows, doors, and other openings.',
            'savings': '$15-30/month',
            'difficulty': 'Moderate',
            'category': 'Insulation'
        }
    ]
    
    if house_type in ["Large House", "Mansion"]:
        tips.append({
            'title': '🏡 Zone Heating/Cooling',
            'description': 'Use programmable thermostats for different zones. Only heat/cool rooms you\'re using.',
            'savings': '$25-50/month',
            'difficulty': 'Moderate',
            'category': 'HVAC'
        })
    
    return tips

def get_house_type_tips(house_type):
    """Tips specific to house type"""
    tips = []
    
    if house_type == "Small Apartment":
        tips.extend([
            {
                'title': '🔥 Efficient Cooking',
                'description': 'Use microwave, toaster oven, or electric kettle instead of conventional oven when possible.',
                'savings': '$5-12/month',
                'difficulty': 'Easy',
                'category': 'Appliances'
            },
            {
                'title': '🪟 Window Treatments',
                'description': 'Use blinds or curtains to block sun in summer and retain heat in winter.',
                'savings': '$8-15/month',
                'difficulty': 'Easy',
                'category': 'Insulation'
            }
        ])
    
    elif house_type in ["Large House", "Mansion"]:
        tips.extend([
            {
                'title': '🏊 Pool Efficiency',
                'description': 'Use a pool cover to reduce evaporation and run the pump during off-peak hours.',
                'savings': '$30-60/month',
                'difficulty': 'Easy',
                'category': 'Pool'
            },
            {
                'title': '🌡️ Smart Zoning',
                'description': 'Install smart thermostats for different zones to avoid heating/cooling unused areas.',
                'savings': '$40-80/month',
                'difficulty': 'Hard',
                'category': 'HVAC'
            }
        ])
    
    return tips

def get_energy_source_tips(energy_source):
    """Tips based on energy source"""
    tips = []
    
    if "Solar" in energy_source:
        tips.extend([
            {
                'title': '☀️ Maximize Solar Usage',
                'description': 'Run major appliances during peak sun hours (10 AM - 4 PM) to use your solar energy directly.',
                'savings': '$20-40/month',
                'difficulty': 'Easy',
                'category': 'Solar'
            },
            {
                'title': '🔋 Battery Storage',
                'description': 'Consider adding battery storage to store excess solar power for evening use.',
                'savings': '$30-60/month',
                'difficulty': 'Hard',
                'category': 'Solar'
            }
        ])
    
    if energy_source == "Grid Electricity":
        tips.append({
            'title': '⏰ Time-of-Use Optimization',
            'description': 'Shift energy-intensive activities to off-peak hours if your utility offers time-of-use rates.',
            'savings': '$15-35/month',
            'difficulty': 'Moderate',
            'category': 'Timing'
        })
    
    return tips

def get_seasonal_tips(season):
    """Seasonal energy-saving tips"""
    tips = []
    
    if season == "Summer":
        tips.extend([
            {
                'title': '🌡️ Summer Cooling Tips',
                'description': 'Use fans to circulate air, close blinds during the day, and cook outdoors when possible.',
                'savings': '$20-35/month',
                'difficulty': 'Easy',
                'category': 'Seasonal'
            },
            {
                'title': '💧 Reduce Hot Water Use',
                'description': 'Take shorter showers and wash clothes in cold water during hot months.',
                'savings': '$10-20/month',
                'difficulty': 'Easy',
                'category': 'Water Heating'
            }
        ])
    
    elif season == "Winter":
        tips.extend([
            {
                'title': '🧥 Layer Up Indoors',
                'description': 'Wear warm clothes indoors and use blankets to stay comfortable at lower temperatures.',
                'savings': '$25-45/month',
                'difficulty': 'Easy',
                'category': 'Seasonal'
            },
            {
                'title': '☀️ Use Natural Heat',
                'description': 'Open curtains on sunny days to let natural heat in, close them at night for insulation.',
                'savings': '$15-25/month',
                'difficulty': 'Easy',
                'category': 'Seasonal'
            }
        ])
    
    return tips

def get_general_tips():
    """General energy-saving tips"""
    return [
        {
            'title': '🔍 Energy Audit',
            'description': 'Conduct a home energy audit to identify specific areas where you can save energy.',
            'savings': '$50-100/month',
            'difficulty': 'Moderate',
            'category': 'Assessment'
        },
        {
            'title': '⭐ Energy Star Appliances',
            'description': 'When replacing appliances, choose Energy Star certified models for maximum efficiency.',
            'savings': '$20-40/month',
            'difficulty': 'Hard',
            'category': 'Appliances'
        },
        {
            'title': '🌱 Programmable Thermostat',
            'description': 'Install a programmable thermostat to automatically adjust temperature based on your schedule.',
            'savings': '$15-30/month',
            'difficulty': 'Moderate',
            'category': 'HVAC'
        }
    ]

def display_tip_card(tip):
    """
    Display a tip as a styled card in Streamlit with dark theme.
    
    Args:
        tip (dict): Tip information dictionary
    """
    # Color coding by difficulty - minimal dark theme colors (grey/green/red only)
    difficulty_colors = {
        'Easy': '#4CAF50',      # Green for easy (good/positive)
        'Moderate': '#b0b0b0',  # Light grey for moderate (neutral)
        'Hard': '#f44336'       # Red for hard (challenging/important)
    }
    
    color = difficulty_colors.get(tip['difficulty'], '#666')
    
    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, rgba(30, 30, 30, 0.8) 0%, rgba(40, 40, 40, 0.6) 100%);
        border: 1px solid #333;
        border-left: 4px solid {color};
        padding: 1.5rem;
        border-radius: 10px;
        margin-bottom: 1rem;
        backdrop-filter: blur(10px);
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.2);
    ">
        <h4 style="color: #f0f0f0; margin-bottom: 0.8rem; font-weight: 400;">{tip['title']}</h4>
        <p style="margin-bottom: 1rem; color: #d0d0d0; line-height: 1.5;">{tip['description']}</p>
        <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 1rem;">
            <span style="background: {color}; color: white; padding: 0.3rem 0.8rem; border-radius: 15px; font-size: 0.85rem; font-weight: 500;">
                {tip['difficulty']}
            </span>
            <span style="font-weight: 600; color: {color}; font-size: 1rem;">
                {tip['savings']}
            </span>
        </div>
    </div>
    """, unsafe_allow_html=True)

def get_tip_categories():
    """Get all available tip categories"""
    return [
        'HVAC', 'Lighting', 'Electronics', 'Water Heating', 
        'Appliances', 'Insulation', 'Solar', 'Seasonal', 
        'Technology', 'Assessment'
    ]

def filter_tips_by_category(tips, category):
    """Filter tips by category"""
    return [tip for tip in tips if tip.get('category') == category]

def calculate_potential_savings(tips):
    """Calculate total potential savings from tips"""
    total_savings = 0
    for tip in tips:
        # Extract numeric value from savings string
        savings_str = tip['savings'].replace('$', '').replace('/month', '')
        if '-' in savings_str:
            # Take average of range
            low, high = savings_str.split('-')
            avg_savings = (float(low) + float(high)) / 2
        else:
            avg_savings = float(savings_str.split()[0])
        
        total_savings += avg_savings
    
    return total_savings
