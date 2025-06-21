"""
Charts Module
Creates beautiful and interactive charts for the energy dashboard.

This module demonstrates:
- Plotly for interactive visualizations
- Data visualization best practices
- Color schemes and styling
- Different chart types (line, bar, pie, scatter)
"""

import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np

# Minimalistic color schemes for dark theme - only black/grey/white with green/red accents
COLORS = {
    'primary': '#e0e0e0',      # Light grey for primary text
    'secondary': '#b0b0b0',    # Medium grey for secondary text
    'accent': '#4CAF50',       # Green for positive/success information
    'success': '#4CAF50',      # Green for success states
    'warning': '#f44336',      # Red for warnings (important info)
    'danger': '#f44336',       # Red for danger/negative states
    'info': '#e0e0e0'          # Light grey for info (no strong colors)
}

# Minimalistic chart colors - shades of grey with green/red for important data
PLOTLY_COLORS = [
    '#e0e0e0',  # Light grey - primary data
    '#b0b0b0',  # Medium grey - secondary data
    '#888888',  # Dark grey - tertiary data
    '#4CAF50',  # Green - positive/good values only
    '#f44336',  # Red - negative/bad values only
    '#cccccc',  # Very light grey
    '#666666'   # Darker grey
]

def create_consumption_chart(energy_data, time_period="Last 30 Days"):
    """
    Create an interactive line chart showing energy consumption over time.
    
    This function demonstrates several key concepts:
    1. Plotly graph creation and customization
    2. Data visualization best practices
    3. Interactive chart features (hover, zoom, pan)
    4. Dark theme implementation
    5. Statistical overlays (average lines, trends)
    
    Args:
        energy_data (pd.DataFrame): Energy consumption data with 'date' and 'consumption' columns
        time_period (str): Time period for the chart title display
    
    Returns:
        plotly.graph_objects.Figure: Interactive line chart with consumption trends
        
    Example:
        >>> chart = create_consumption_chart(energy_data, "Last 30 Days")
        >>> st.plotly_chart(chart, use_container_width=True)
    """
    # Create a new Plotly figure object
    # This is the foundation for all chart elements
    fig = go.Figure()
    
    # Add the main consumption trend line
    # Using go.Scatter with mode='lines+markers' creates an interactive line chart
    fig.add_trace(go.Scatter(
        x=energy_data['date'],           # X-axis: dates
        y=energy_data['consumption'],    # Y-axis: consumption values
        mode='lines+markers',            # Display both lines and data points
        name='Daily Consumption',        # Legend label
        line=dict(color=COLORS['primary'], width=3),  # Line styling
        marker=dict(size=6, color=COLORS['primary']), # Marker styling
        # Custom hover template for better user experience
        hovertemplate='<b>%{x}</b><br>Consumption: %{y:.1f} kWh<extra></extra>'
    ))
    
    # Add horizontal reference line showing average consumption
    # This helps users understand their performance relative to average
    avg_consumption = energy_data['consumption'].mean()
    fig.add_hline(
        y=avg_consumption,                    # Y position of the line
        line_dash="dash",                     # Dashed line style
        line_color=COLORS['accent'],          # Line color
        annotation_text=f"Average: {avg_consumption:.1f} kWh",  # Label
        annotation_position="top right"       # Label position
    )
    
    # Add trend line using linear regression
    # This demonstrates basic statistical analysis and numpy usage
    if len(energy_data) > 7:  # Only add trend if enough data points
        # Use numpy's polyfit to calculate linear trend
        # polyfit returns coefficients for polynomial (linear in this case)
        z = np.polyfit(range(len(energy_data)), energy_data['consumption'], 1)
        p = np.poly1d(z)  # Create polynomial function from coefficients
        
        # Calculate trend line y-values for all x-positions
        trend_y = [p(i) for i in range(len(energy_data))]
        
        # Add trend line to the chart
        fig.add_trace(go.Scatter(
            x=energy_data['date'],
            y=trend_y,
            mode='lines',                     # Only lines, no markers
            name='Trend',
            line=dict(color=COLORS['warning'], width=2, dash='dot'),
            hovertemplate='Trend: %{y:.1f} kWh<extra></extra>'
        ))
    
    # Customize the chart layout for dark theme and professional appearance
    fig.update_layout(
        title=f'Energy Consumption Trend - {time_period}',
        xaxis_title='Date',
        yaxis_title='Consumption (kWh)',
        hovermode='x unified',              # Show all hover info at once
        showlegend=True,                    # Display legend
        height=400,                         # Chart height
        # Dark theme colors
        plot_bgcolor='rgba(0,0,0,0)',       # Transparent plot background
        paper_bgcolor='rgba(0,0,0,0)',      # Transparent paper background
        font=dict(family="Arial", size=12, color='#e0e0e0'),  # Font styling
        title_font=dict(size=16, color='#f0f0f0')  # Title font
    )
    
    # Customize grid lines for better readability
    fig.update_xaxes(
        showgrid=True,                      # Show vertical grid lines
        gridwidth=1,                        # Grid line width
        gridcolor='rgba(128,128,128,0.2)'   # Subtle grid color
    )
    fig.update_yaxes(
        showgrid=True,                      # Show horizontal grid lines
        gridwidth=1,
        gridcolor='rgba(128,128,128,0.2)'
    )
    
    return fig

def create_appliance_breakdown(appliance_data):
    """
    Create a pie chart showing energy consumption by appliance.
    
    Args:
        appliance_data (pd.DataFrame): Appliance consumption data
    
    Returns:
        plotly.graph_objects.Figure: Interactive pie chart
    """
    fig = go.Figure(data=[go.Pie(
        labels=appliance_data['appliance'],
        values=appliance_data['daily_kwh'],
        hole=0.4,
        textinfo='label+percent',
        textposition='auto',
        marker_colors=PLOTLY_COLORS,
        hovertemplate='<b>%{label}</b><br>Consumption: %{value:.1f} kWh<br>Percentage: %{percent}<extra></extra>'
    )])
    
    fig.update_layout(
        title='Energy Consumption by Appliance',
        showlegend=True,
        height=400,
        # Dark theme styling
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family="Arial", size=12, color='#e0e0e0'),
        title_font=dict(size=16, color='#f0f0f0'),
        legend=dict(
            orientation="v", 
            yanchor="middle", 
            y=0.5, 
            xanchor="left", 
            x=1.05,
            font=dict(color='#e0e0e0')
        )
    )
    
    return fig

def create_cost_analysis(energy_data, rate_per_kwh=0.12):
    """
    Create a chart showing cost analysis over time.
    
    Args:
        energy_data (pd.DataFrame): Energy consumption data
        rate_per_kwh (float): Cost per kWh
    
    Returns:
        plotly.graph_objects.Figure: Cost analysis chart
    """
    # Calculate costs
    energy_data = energy_data.copy()
    energy_data['daily_cost'] = energy_data['consumption'] * rate_per_kwh
    energy_data['cumulative_cost'] = energy_data['daily_cost'].cumsum()
    
    # Create subplot with secondary y-axis
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    
    # Add daily cost bars
    fig.add_trace(
        go.Bar(
            x=energy_data['date'],
            y=energy_data['daily_cost'],
            name='Daily Cost',
            marker_color=COLORS['info'],
            opacity=0.7,
            hovertemplate='<b>%{x}</b><br>Daily Cost: $%{y:.2f}<extra></extra>'
        ),
        secondary_y=False,
    )
    
    # Add cumulative cost line
    fig.add_trace(
        go.Scatter(
            x=energy_data['date'],
            y=energy_data['cumulative_cost'],
            mode='lines+markers',
            name='Cumulative Cost',
            line=dict(color=COLORS['danger'], width=3),
            marker=dict(size=4),
            hovertemplate='<b>%{x}</b><br>Total Cost: $%{y:.2f}<extra></extra>'
        ),
        secondary_y=True,
    )
    
    # Set y-axes titles
    fig.update_yaxes(title_text="Daily Cost ($)", secondary_y=False)
    fig.update_yaxes(title_text="Cumulative Cost ($)", secondary_y=True)
    
    fig.update_layout(
        title='Energy Cost Analysis',
        xaxis_title='Date',
        hovermode='x unified',
        height=400,
        # Dark theme styling
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family="Arial", size=12, color='#e0e0e0'),
        title_font=dict(size=16, color='#f0f0f0')
    )
    
    return fig

def create_hourly_pattern_chart(hourly_data):
    """
    Create a chart showing hourly consumption patterns.
    
    Args:
        hourly_data (pd.DataFrame): Hourly consumption data
    
    Returns:
        plotly.graph_objects.Figure: Hourly pattern chart
    """
    fig = go.Figure()
    
    # Color code by time period
    colors = {
        'Night': COLORS['primary'],
        'Morning': COLORS['warning'],
        'Afternoon': COLORS['info'],
        'Evening': COLORS['danger']
    }
    
    for period in hourly_data['period'].unique():
        period_data = hourly_data[hourly_data['period'] == period]
        
        fig.add_trace(go.Bar(
            x=period_data['time'],
            y=period_data['consumption'],
            name=period,
            marker_color=colors.get(period, COLORS['accent']),
            hovertemplate='<b>%{x}</b><br>%{y:.2f} kWh<br>Period: ' + period + '<extra></extra>'
        ))
    
    fig.update_layout(
        title='Hourly Energy Consumption Pattern',
        xaxis_title='Time of Day',
        yaxis_title='Consumption (kWh)',
        height=400,
        barmode='group',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family="Arial", size=12),
        title_font=dict(size=16, color=COLORS['primary'])
    )
    
    return fig

def create_efficiency_comparison(appliance_data):
    """
    Create a chart comparing appliance efficiency ratings.
    
    Args:
        appliance_data (pd.DataFrame): Appliance data with efficiency ratings
    
    Returns:
        plotly.graph_objects.Figure: Efficiency comparison chart
    """
    # Convert efficiency ratings to numeric scores
    efficiency_scores = {
        'A+++': 10, 'A++': 9, 'A+': 8, 'A': 7, 'B': 6, 'C': 5, 'D': 4
    }
    
    appliance_data = appliance_data.copy()
    appliance_data['efficiency_score'] = appliance_data['efficiency_rating'].map(efficiency_scores)
    
    fig = go.Figure()
    
    # Create bubble chart
    fig.add_trace(go.Scatter(
        x=appliance_data['daily_kwh'],
        y=appliance_data['efficiency_score'],
        mode='markers+text',
        marker=dict(
            size=appliance_data['daily_cost'] * 5,  # Size based on cost
            color=appliance_data['efficiency_score'],
            colorscale='RdYlGn',
            showscale=True,
            colorbar=dict(title="Efficiency Score")
        ),
        text=appliance_data['appliance'],
        textposition='top center',
        hovertemplate='<b>%{text}</b><br>Consumption: %{x:.1f} kWh<br>Efficiency: %{y}/10<extra></extra>'
    ))
    
    fig.update_layout(
        title='Appliance Efficiency vs Consumption',
        xaxis_title='Daily Consumption (kWh)',
        yaxis_title='Efficiency Score (10 = Best)',
        height=500,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family="Arial", size=12),
        title_font=dict(size=16, color=COLORS['primary'])
    )
    
    return fig

def create_seasonal_analysis(energy_data):
    """
    Create a chart showing seasonal energy consumption patterns.
    
    Args:
        energy_data (pd.DataFrame): Energy data with season information
    
    Returns:
        plotly.graph_objects.Figure: Seasonal analysis chart
    """
    seasonal_data = energy_data.groupby('season')['consumption'].agg(['mean', 'std']).reset_index()
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=seasonal_data['season'],
        y=seasonal_data['mean'],
        error_y=dict(type='data', array=seasonal_data['std']),
        name='Average Consumption',
        marker_color=PLOTLY_COLORS,
        hovertemplate='<b>%{x}</b><br>Average: %{y:.1f} kWh<extra></extra>'
    ))
    
    fig.update_layout(
        title='Seasonal Energy Consumption Analysis',
        xaxis_title='Season',
        yaxis_title='Average Consumption (kWh)',
        height=400,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family="Arial", size=12),
        title_font=dict(size=16, color=COLORS['primary'])
    )
    
    return fig

def create_comparison_chart(data_dict, title="Comparison"):
    """
    Create a comparison chart for multiple datasets.
    
    Args:
        data_dict (dict): Dictionary with labels as keys and values as data
        title (str): Chart title
    
    Returns:
        plotly.graph_objects.Figure: Comparison chart
    """
    fig = go.Figure()
    
    colors = PLOTLY_COLORS[:len(data_dict)]
    
    for i, (label, values) in enumerate(data_dict.items()):
        fig.add_trace(go.Bar(
            name=label,
            x=list(range(len(values))),
            y=values,
            marker_color=colors[i % len(colors)]
        ))
    
    fig.update_layout(
        title=title,
        xaxis_title='Time Period',
        yaxis_title='Value',
        barmode='group',
        height=400,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family="Arial", size=12),
        title_font=dict(size=16, color=COLORS['primary'])
    )
    
    return fig
