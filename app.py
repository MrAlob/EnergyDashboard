"""
Energy Dashboard - Main Application
A beautiful and interactive energy consumption dashboard with modern minimalistic design.

This dashboard showcases Python's capabilities for:
- Data visualization and analysis
- Web application development
- Interactive user interfaces
- Real-time data processing and insights
"""

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import pandas as pd
import numpy as np

# Import our custom components
from components.data_generator import generate_energy_data, generate_appliance_data
from components.charts import create_consumption_chart, create_appliance_breakdown, create_cost_analysis
from components.tips import get_energy_tips, display_tip_card

# Configure the Streamlit page
st.set_page_config(
    page_title="🔋 Energy Dashboard",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load custom CSS
def load_css():
    """Load custom CSS for dark minimalistic styling"""
    st.markdown("""
    <style>
    /* Dark theme base - glossy black background */
    .stApp {
        background: linear-gradient(135deg, #0a0a0a 0%, #1a1a1a 100%);
        color: #e0e0e0;
    }
    
    .main .block-container {
        background: transparent;
        padding-top: 2rem;
        color: #e0e0e0;
    }
    
    /* Main header styling - dark elegant */
    .main-header {
        background: linear-gradient(135deg, #1a1a1a 0%, #2a2a2a 100%);
        border: 1px solid #333;
        padding: 2rem;
        border-radius: 15px;
        color: #f0f0f0;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.5);
        backdrop-filter: blur(10px);
    }
    
    .main-header h1 {
        color: #ffffff;
        margin-bottom: 0.5rem;
        font-size: 2.5rem;
        font-weight: 300;
        letter-spacing: 2px;
    }
    
    .main-header p {
        color: #b0b0b0;
        font-size: 1.1rem;
        margin-bottom: 0;
        font-weight: 300;
    }
    
    /* Metric cards - dark glass effect */
    .stMetric {
        background: linear-gradient(135deg, rgba(30, 30, 30, 0.8) 0%, rgba(50, 50, 50, 0.6) 100%);
        border: 1px solid #333;
        padding: 1.5rem;
        border-radius: 12px;
        color: #e0e0e0;
        backdrop-filter: blur(10px);
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.3);
    }
    
    .stMetric [data-testid="metric-container"] {
        background: transparent;
        border: none;
    }
    
    .stMetric [data-testid="metric-container"] > div {
        color: #e0e0e0;
    }
    
    /* Success/positive values in subtle green */
    .stMetric [data-testid="metric-container"] [data-testid="metric-delta"] {
        color: #4CAF50 !important;
    }
    
    /* Sidebar styling - dark */
    .stSidebar {
        background: linear-gradient(180deg, #1a1a1a 0%, #0a0a0a 100%);
    }
    
    .stSidebar > div {
        background: transparent;
    }
    
    .stSidebar .stSelectbox > div > div {
        background: rgba(40, 40, 40, 0.8);
        border: 1px solid #444;
        color: #e0e0e0;
    }
    
    .stSidebar .stSelectbox label {
        color: #b0b0b0;
    }
    
    /* Button styling - minimal dark */
    .stButton > button {
        background: linear-gradient(135deg, #2a2a2a 0%, #3a3a3a 100%);
        color: #e0e0e0;
        border: 1px solid #444;
        border-radius: 8px;
        padding: 0.75rem 1.5rem;
        font-weight: 400;
        transition: all 0.3s ease;
        backdrop-filter: blur(10px);
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #3a3a3a 0%, #4a4a4a 100%);
        border-color: #555;
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.4);
    }
    
    /* Tab styling - dark */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: transparent;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: rgba(30, 30, 30, 0.6);
        border: 1px solid #333;
        color: #b0b0b0;
        padding: 0.8rem 1.5rem;
        border-radius: 8px;
        transition: all 0.2s ease;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background: rgba(40, 40, 40, 0.8);
        border-color: #444;
        color: #e0e0e0;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #2a2a2a 0%, #3a3a3a 100%);
        color: #ffffff !important;
        border-color: #555;
    }
    
    /* Chart containers - dark theme */
    .js-plotly-plot .plotly {
        background: rgba(20, 20, 20, 0.8) !important;
        border-radius: 12px;
        border: 1px solid #333;
    }
    
    .js-plotly-plot .plotly .modebar {
        background: rgba(30, 30, 30, 0.9) !important;
        border-radius: 6px;
    }
    
    /* Info boxes - dark with colored accents */
    .stInfo {
        background: linear-gradient(135deg, rgba(30, 30, 30, 0.8) 0%, rgba(40, 40, 40, 0.6) 100%);
        border: 1px solid #444;
        border-left: 4px solid #2196F3;
        color: #e0e0e0;
        backdrop-filter: blur(10px);
    }
    
    .stSuccess {
        background: linear-gradient(135deg, rgba(30, 30, 30, 0.8) 0%, rgba(40, 40, 40, 0.6) 100%);
        border: 1px solid #444;
        border-left: 4px solid #4CAF50;
        color: #e0e0e0;
        backdrop-filter: blur(10px);
    }
    
    .stWarning {
        background: linear-gradient(135deg, rgba(30, 30, 30, 0.8) 0%, rgba(40, 40, 40, 0.6) 100%);
        border: 1px solid #444;
        border-left: 4px solid #FF9800;
        color: #e0e0e0;
        backdrop-filter: blur(10px);
    }
    
    .stError {
        background: linear-gradient(135deg, rgba(30, 30, 30, 0.8) 0%, rgba(40, 40, 40, 0.6) 100%);
        border: 1px solid #444;
        border-left: 4px solid #f44336;
        color: #e0e0e0;
        backdrop-filter: blur(10px);
    }
    
    /* Expander styling - dark */
    .streamlit-expanderHeader {
        background: rgba(30, 30, 30, 0.8);
        border: 1px solid #333;
        color: #e0e0e0;
        border-radius: 8px;
    }
    
    .streamlit-expanderContent {
        background: rgba(20, 20, 20, 0.9);
        border: 1px solid #333;
        border-top: none;
        color: #e0e0e0;
    }
    
    /* Text colors */
    h1, h2, h3, h4, h5, h6 {
        color: #f0f0f0 !important;
    }
    
    p, div, span {
        color: #e0e0e0;
    }
    
    /* Scrollbar dark theme */
    ::-webkit-scrollbar {
        width: 8px;
        background: #1a1a1a;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #333 0%, #555 100%);
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(135deg, #444 0%, #666 100%);
    }
    
    /* Remove Streamlit branding */
    .viewerBadge_container__1QSob {
        display: none !important;
    }
    
    #MainMenu {
        display: none !important;
    }
    
    footer {
        display: none !important;
    }
    
    header {
        display: none !important;
    }
    </style>
    """, unsafe_allow_html=True)

def main():
    """
    Main application function that orchestrates the entire dashboard.
    
    This function demonstrates several key Python concepts:
    1. Function organization and modular design
    2. Streamlit web app structure
    3. Data processing and visualization
    4. User interface creation
    5. Interactive elements and state management
    """
    # Load custom CSS for dark theme styling
    load_css()
    
    # === HEADER SECTION ===
    # Create the main header using HTML and CSS for custom styling
    # This shows how to embed HTML in Streamlit for advanced layouts
    st.markdown("""
    <div class="main-header">
        <h1>ENERGY DASHBOARD</h1>
        <p>Monitor • Analyze • Optimize</p>
    </div>
    """, unsafe_allow_html=True)
    
    # === SIDEBAR CONTROLS ===
    # Streamlit's sidebar feature for user input controls
    # This demonstrates form elements and user interaction
    with st.sidebar:
        st.markdown("## Controls")
        
        # Selectbox widgets for user input
        # These control the data generation and analysis
        st.markdown("### Time Period")
        time_period = st.selectbox(
            "Select period:",
            ["Last 7 Days", "Last 30 Days", "Last 3 Months", "Last Year"]
        )
        
        st.markdown("### House Profile")
        house_type = st.selectbox(
            "House type:",
            ["Small Apartment", "Medium House", "Large House", "Mansion"]
        )
        
        energy_source = st.selectbox(
            "Primary source:",
            ["Grid Electricity", "Solar + Grid", "Solar Only", "Wind + Grid"]
        )
        
        # Button to refresh data - demonstrates state management
        if st.button("Refresh Data", type="primary"):
            st.cache_data.clear()  # Clear Streamlit's cache
            st.rerun()  # Reload the app with new data
    
    # === DATA GENERATION ===
    # Convert user selections into data parameters
    # This demonstrates dictionary lookups and data processing
    days = {"Last 7 Days": 7, "Last 30 Days": 30, "Last 3 Months": 90, "Last Year": 365}[time_period]
    
    # Generate sample data based on user selections
    # These functions demonstrate data simulation and pandas usage
    energy_data = generate_energy_data(days=days, house_type=house_type)
    appliance_data = generate_appliance_data(house_type=house_type)
    
    # === KEY METRICS SECTION ===
    # Create a responsive layout with columns
    # This demonstrates Streamlit's layout system
    col1, col2, col3, col4 = st.columns(4)
    
    # Calculate key performance indicators (KPIs)
    # This shows basic statistical calculations and business logic
    current_usage = energy_data['consumption'].iloc[-1]  # Latest value
    avg_usage = energy_data['consumption'].mean()        # Average calculation
    total_cost = (energy_data['consumption'] * 0.12).sum()  # Cost calculation
    savings_potential = total_cost * 0.15  # 15% potential savings estimate
    
    # Display metrics using Streamlit's metric widget
    # Each metric shows current value and delta (change from baseline)
    with col1:
        st.metric(
            "Current Usage",
            f"{current_usage:.1f} kWh",
            delta=f"{current_usage - avg_usage:.1f}",
            delta_color="inverse"  # Red for higher usage
        )
    
    with col2:
        st.metric(
            "Average Daily",
            f"{avg_usage:.1f} kWh",
            delta="Baseline"
        )
    
    with col3:
        st.metric(
            "Total Cost",
            f"${total_cost:.2f}",
            delta=f"-${savings_potential:.2f} potential"
        )
    
    with col4:
        # Calculate efficiency score (0-100 scale)
        efficiency_score = max(0, 100 - (current_usage / avg_usage - 1) * 100)
        st.metric(
            "Efficiency Score",
            f"{efficiency_score:.0f}/100",
            delta=f"{efficiency_score - 75:.0f} vs target"
        )
    
    # === CHARTS AND ANALYSIS SECTION ===
    # Streamlit tabs for organized content presentation
    st.markdown("## Analysis")
    
    tab1, tab2, tab3 = st.tabs(["Consumption", "Breakdown", "Cost Analysis"])
    
    # Tab 1: Consumption Trends
    with tab1:
        # Two-column layout for chart and insights
        col1, col2 = st.columns([2, 1])
        
        with col1:
            # Generate and display interactive chart
            # This demonstrates plotly integration with Streamlit
            fig = create_consumption_chart(energy_data, time_period)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("### Insights")
            
            # Data analysis to find peak usage patterns
            # This shows pandas data manipulation and analysis
            peak_day = energy_data.loc[energy_data['consumption'].idxmax(), 'date']
            peak_usage = energy_data['consumption'].max()
            
            # Display insights using info boxes
            st.info(f"""
            **Peak Usage:** {peak_day.strftime('%B %d')}
            
            **Peak Consumption:** {peak_usage:.1f} kWh
            
            **Trend:** {'Increasing' if energy_data['consumption'].iloc[-7:].mean() > energy_data['consumption'].iloc[:-7].mean() else 'Decreasing'}
            """)
            
            # Weekly pattern analysis
            # This demonstrates groupby operations and statistical analysis
            energy_data['weekday'] = energy_data['date'].dt.day_name()
            weekly_avg = energy_data.groupby('weekday')['consumption'].mean()
            highest_day = weekly_avg.idxmax()
            
            st.success(f"""
            **Highest Day:** {highest_day}
            
            **Pattern:** {'Weekend higher' if weekly_avg[['Saturday', 'Sunday']].mean() > weekly_avg[['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']].mean() else 'Weekday higher'}
            """)
    
    # Tab 2: Appliance Breakdown
    with tab2:
        col1, col2 = st.columns([1, 1])
        
        with col1:
            # Pie chart for appliance consumption distribution
            fig_pie = create_appliance_breakdown(appliance_data)
            st.plotly_chart(fig_pie, use_container_width=True)
        
        with col2:
            # Horizontal bar chart for detailed view
            # This demonstrates different chart types and data sorting
            fig_bar = px.bar(
                appliance_data.sort_values('daily_kwh', ascending=True),
                x='daily_kwh',
                y='appliance',
                orientation='h',
                title="Daily Consumption by Appliance",
                color='daily_kwh',
                color_continuous_scale=[[0, '#666666'], [0.5, '#b0b0b0'], [1, '#e0e0e0']]  # Minimal grey scale
            )
            fig_bar.update_layout(
                height=400,
                showlegend=False,
                plot_bgcolor='rgba(0,0,0,0)',  # Transparent background
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#e0e0e0'),  # Light text for dark theme
                title_font=dict(color='#f0f0f0')
            )
            st.plotly_chart(fig_bar, use_container_width=True)
    
    # Tab 3: Cost Analysis
    with tab3:
        # Main cost analysis chart
        fig_cost = create_cost_analysis(energy_data)
        st.plotly_chart(fig_cost, use_container_width=True)
        
        # Cost breakdown section
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### Cost Breakdown")
            
            # Calculate costs for different time periods
            # This demonstrates mathematical calculations and data scaling
            monthly_cost = total_cost * 30 / days
            yearly_cost = monthly_cost * 12
            
            # Create cost comparison data
            cost_data = pd.DataFrame({
                'Period': ['Daily', 'Monthly', 'Yearly'],
                'Cost': [total_cost/days, monthly_cost, yearly_cost]
            })
            
            # Bar chart for cost comparison
            fig_cost_bar = px.bar(
                cost_data,
                x='Period',
                y='Cost',
                title="Average Energy Costs",
                color='Cost',
                color_continuous_scale=[[0, '#b0b0b0'], [0.5, '#f44336'], [1, '#f44336']]  # Grey to red for costs
            )
            fig_cost_bar.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#e0e0e0'),
                title_font=dict(color='#f0f0f0')
            )
            st.plotly_chart(fig_cost_bar, use_container_width=True)
        
        with col2:
            st.markdown("### Savings Opportunities")
            
            # Sample data for investment vs savings analysis
            # This demonstrates creating structured data for analysis
            savings_data = pd.DataFrame({
                'Strategy': ['LED Upgrades', 'Smart Thermostat', 'Energy Star Appliances', 'Solar Panels'],
                'Monthly Savings': [15, 25, 30, 85],
                'Investment': [200, 300, 1500, 15000]
            })
            
            # Scatter plot to show investment vs return relationship
            fig_savings = px.scatter(
                savings_data,
                x='Investment',
                y='Monthly Savings',
                size='Monthly Savings',
                color='Strategy',
                title="Investment vs Monthly Savings",
                hover_data=['Strategy']
            )
            fig_savings.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#e0e0e0'),
                title_font=dict(color='#f0f0f0')
            )
            st.plotly_chart(fig_savings, use_container_width=True)
    
    # === ENERGY TIPS SECTION ===
    # Personalized recommendations based on user data
    st.markdown("## Energy Tips")
    
    # Generate personalized tips based on usage patterns
    # This demonstrates conditional logic and data-driven recommendations
    tips = get_energy_tips(house_type, energy_source, current_usage, avg_usage)
    
    # Display top tips in a grid layout
    cols = st.columns(3)
    for i, tip in enumerate(tips[:3]):
        with cols[i % 3]:
            display_tip_card(tip)
    
    # Additional tips in expandable section
    # This demonstrates progressive disclosure UI pattern
    with st.expander("More Tips"):
        for tip in tips[3:]:
            display_tip_card(tip)
    
    # === FOOTER ===
    # Minimal separator only - no branding or technology mentions
    st.markdown("---")

if __name__ == "__main__":
    main()
