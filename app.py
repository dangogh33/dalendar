#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 17 19:17:00 2025

@author: danbickelhaupt
"""

import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import datetime
from matplotlib.patches import Wedge, Circle, Rectangle

def create_circular_calendar(year=2025, start_date=None, current_date=None, figsize=(14,14)):
    # If no start_date provided, use January 1st of the given year
    if start_date is None:
        start_date = datetime.date(year, 1, 1)
    
    # If no current_date provided, use today's date
    if current_date is None:
        current_date = datetime.date.today()
    
    # Colors
    bg_color = 'black'
    completed_color = '#00FF00'  # Bright green
    current_color = 'white'
    outline_color = '#006600'    # Darker green
    month_label_color = '#00AA00'  # Medium green
    trad_month_color = '#00FFAA'  # Brighter green for traditional month outlines
    
    # Create figure
    fig, ax = plt.subplots(figsize=figsize, facecolor=bg_color)
    ax.set_aspect('equal')
    ax.set_facecolor(bg_color)
    
    # Calculate total days and weeks
    total_weeks = 13 * 4  # 13 months of 4 weeks
    total_days = total_weeks * 7  # Each week has 7 days
    
    # Calculate days since start
    days_since_start = (current_date - start_date).days
    
    # Radius parameters
    outer_radius = 10
    inner_radius = 2
    
    # Divide circle into weeks - clockwise from top (12 o'clock position)
    angle_per_week = 360 / total_weeks
    
    # Calculate days within each week
    days_of_week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    day_radius_width = (outer_radius - inner_radius) / 7
    
    # Track traditional month boundaries
    traditional_months = []
    current_month = start_date.month
    
    # Draw weeks as sectors, with days within each week
    for week_idx in range(total_weeks):
        week_start_date = start_date + datetime.timedelta(days=week_idx*7)
        
        # Calculate angles for this week (clockwise from top)
        # Start at 90 degrees (top/12 o'clock) and move clockwise
        week_start_angle = 90 - week_idx * angle_per_week
        week_end_angle = week_start_angle - angle_per_week
        
        # Ensure angles are properly ordered (start > end for clockwise)
        if week_start_angle < week_end_angle:
            week_start_angle += 360
            
        # Add week number label - HORIZONTAL
        week_angle = (week_start_angle + week_end_angle) / 2
        week_radius = outer_radius + 0.3
        week_x = week_radius * np.cos(np.radians(week_angle))
        week_y = week_radius * np.sin(np.radians(week_angle))
        
        ax.text(week_x, week_y, f"W{week_idx+1}", color=month_label_color, 
               ha='center', va='center', fontsize=8, fontweight='bold',
               rotation=0)  # Always horizontal
        
        # Draw days within this week
        for day_idx in range(7):
            day_date = week_start_date + datetime.timedelta(days=day_idx)
            
            # Track traditional month boundaries
            if day_date.month != current_month:
                current_month = day_date.month
                days_from_start = (day_date - start_date).days
                traditional_months.append((day_date.strftime('%b'), days_from_start))
            
            # Calculate radius for this day (Sunday innermost, Monday outermost)
            day_outer_radius = outer_radius - day_idx * day_radius_width
            day_inner_radius = day_outer_radius - day_radius_width
            
            # Determine color based on date
            days_from_calendar_start = (day_date - start_date).days
            if days_from_calendar_start < days_since_start:
                color = completed_color  # Past day (green)
            elif days_from_calendar_start == days_since_start:
                color = current_color    # Current day (white)
            else:
                color = bg_color         # Future day (black)
            
            # Create wedge for this day
            wedge = Wedge((0, 0), day_outer_radius, week_end_angle, week_start_angle, 
                          width=day_radius_width, facecolor=color, 
                          edgecolor=outline_color, linewidth=0.5)
            ax.add_patch(wedge)
    
    # Draw traditional month ticks and labels (moved to be between ticks)
    for i in range(len(traditional_months)):
        month_name, day_offset = traditional_months[i]
        
        # Calculate the week and day within week
        week_idx = day_offset // 7
        day_in_week = day_offset % 7
        
        # Calculate angle for this tick mark
        tick_angle = 90 - week_idx * angle_per_week
        
        # Draw a tick mark at the outer radius
        tick_length = 0.3
        x1 = outer_radius * np.cos(np.radians(tick_angle))
        y1 = outer_radius * np.sin(np.radians(tick_angle))
        x2 = (outer_radius + tick_length) * np.cos(np.radians(tick_angle))
        y2 = (outer_radius + tick_length) * np.sin(np.radians(tick_angle))
        ax.plot([x1, x2], [y1, y2], color=trad_month_color, linestyle='-', linewidth=2)
        
        # Calculate the midpoint between this tick and the next one for label
        if i < len(traditional_months) - 1:
            next_day_offset = traditional_months[i+1][1]
            next_week_idx = next_day_offset // 7
            next_angle = 90 - next_week_idx * angle_per_week
        else:
            # For the last month, use the first month of the next year
            next_angle = -270  # 90 degrees - 360 degrees
        
        # Make sure angles are properly ordered for midpoint calculation
        if next_angle > tick_angle:
            next_angle -= 360
        
        mid_angle = (tick_angle + next_angle) / 2
        
        # Add traditional month label
        label_radius = outer_radius + 0.6
        x = label_radius * np.cos(np.radians(mid_angle))
        y = label_radius * np.sin(np.radians(mid_angle))
        ax.text(x, y, month_name, color=trad_month_color, ha='center', va='center', 
                fontsize=10, fontweight='bold', rotation=0)
    
    # Add 13-month calendar month labels - ALWAYS HORIZONTAL
    for month_idx in range(13):
        month_start_week = month_idx * 4
        month_end_week = month_start_week + 4
        
        # Calculate angles for this month (clockwise from top)
        month_start_angle = 90 - month_start_week * angle_per_week
        month_end_angle = 90 - month_end_week * angle_per_week
        if month_start_angle < month_end_angle:
            month_start_angle += 360
            
        month_mid_angle = (month_start_angle + month_end_angle) / 2
        
        # Add month label at middle radius - NO ROTATION
        mid_radius = (inner_radius + outer_radius) / 2
        month_x = mid_radius * np.cos(np.radians(month_mid_angle))
        month_y = mid_radius * np.sin(np.radians(month_mid_angle))
            
        ax.text(month_x, month_y, f"M{month_idx+1}", color=month_label_color, 
               ha='center', va='center', fontsize=12, fontweight='bold',
               rotation=0)  # Always horizontal
        
        # Draw line from inner to outer radius for each 13-month calendar month (except first)
        if month_idx > 0:  # Skip first boundary (it's the same as the last)
            boundary_angle = 90 - month_start_week * angle_per_week
            
            # Draw a line from inner to outer radius
            x1 = inner_radius * np.cos(np.radians(boundary_angle))
            y1 = inner_radius * np.sin(np.radians(boundary_angle))
            x2 = outer_radius * np.cos(np.radians(boundary_angle))
            y2 = outer_radius * np.sin(np.radians(boundary_angle))
            ax.plot([x1, x2], [y1, y2], color='#00CC00', linestyle='-', linewidth=1)
    
    # Add title
    # plt.title('13-Month Circular Calendar', color=month_label_color, fontsize=20, pad=20)
    
    # Set limits and remove axes
    ax.set_xlim(-outer_radius-3, outer_radius+3)
    ax.set_ylim(-outer_radius-3, outer_radius+3)
    ax.axis('off')
    
    # Add central circle
    center = Circle((0, 0), inner_radius, facecolor=bg_color, edgecolor=outline_color)
    ax.add_patch(center)
    
    # Add year in center
    ax.text(0, 0, str(year), color=month_label_color, ha='center', va='center', 
            fontsize=16, fontweight='bold')
    
    # Add a day labels around the outside
    # Labels at each ring level
    for i, day in enumerate(['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']):
        day_radius = outer_radius - i * day_radius_width - day_radius_width/2
        # Position label at 135 degrees (upper left)
        label_angle = 135
        x = day_radius * np.cos(np.radians(label_angle))
        y = day_radius * np.sin(np.radians(label_angle))
        ax.text(x, y, day, color=month_label_color, fontsize=8, 
                ha='center', va='center', rotation=0)
    
    # Add a retro computer terminal style to the figure
    # Add scan lines
    for y in np.linspace(-outer_radius-3, outer_radius+3, 100):
        ax.axhline(y, color='#003300', alpha=0.1, linewidth=0.5)
    
    # Add a CRT-like frame
    frame = Rectangle((-outer_radius-3, -outer_radius-3), 
                      2*(outer_radius+3), 2*(outer_radius+3),
                      fill=False, edgecolor='#005500', linewidth=3)
    ax.add_patch(frame)
    
    # Add current date indicator in corner
    date_str = current_date.strftime("%Y-%m-%d")
    ax.text(-outer_radius-2.5, -outer_radius-2.5, f"TODAY: {date_str}", color='#00FF00', 
            fontsize=10, family='monospace')
    
    # Add start date indicator in opposite corner
    start_date_str = start_date.strftime("%Y-%m-%d")
    ax.text(outer_radius-2.5, -outer_radius-2.5, f"START: {start_date_str}", color='#00FF00', 
            fontsize=10, family='monospace', ha='right')
    
    plt.tight_layout()
    
    return fig

def monday_closest_to_jan1():
    # Get current year
    current_year = datetime.datetime.now().year
    
    # Create date object for January 1st of current year
    jan1 = datetime.date(current_year, 1, 1)
    
    # Get the day of the week (0 is Monday, 6 is Sunday)
    day_of_week = jan1.weekday()
    
    # Calculate days to nearest Monday on or before Jan 1
    if day_of_week == 0:  # If Jan 1 is already Monday
        return jan1
    else:  # For any other day, go backward to previous Monday
        return jan1 - datetime.timedelta(days=day_of_week)

# # Create and save the calendar
# fig = create_circular_calendar(year=datetime.datetime.now().year, start_date=monday_closest_to_jan1())
# plt.savefig('circular_calendar.png', dpi=300, facecolor='black')
# plt.show()

# Streamlit app
st.set_page_config(page_title="The Dalendar", layout="wide")
st.title(f"The Dalendar for {datetime.datetime.now().year}")

# Add some interactive controls
col2 = st.columns([3])

# with col1:
    # year = st.number_input("Year", min_value=2020, max_value=2030, value=2025)
    # today = datetime.date.today()
    # use_today = st.checkbox("Use today's date", value=True)
    
    # if not use_today:
    #     month = st.selectbox("Month", range(1, 13), today.month - 1)
    #     day = st.selectbox("Day", range(1, 32), min(today.day - 1, 30))
    #     selected_date = datetime.date(year, month, day)
    # else:
    #     selected_date = today

# Create the calendar
today = datetime.date.today()
fig = create_circular_calendar(year=today.year, current_date=today, figsize=(12,12))

# Display the calendar
with col2:
    st.pyplot(fig, use_container_width=True)

# Add explanation
st.markdown("""
## About This Calendar
This calendar divides the year into 13 months of exactly 4 weeks (28 days) each.
- **M1-M13**: The 13 equal months
- **W1-W52**: The 52 weeks of the year
- **Green sections**: Completed days
- **White section**: Current day
""")