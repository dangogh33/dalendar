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
import calendar
import pandas as pd

def get_today_central():
    """Get the current date in US Central timezone using pandas."""
    # Create a timestamp in UTC
    now_utc = pd.Timestamp.now(tz='UTC')
    
    # Convert to US Central timezone
    now_central = now_utc.tz_convert('US/Central')
    
    # Extract date only (no time component)
    return now_central.date()

def is_leap_day(date):
    """Check if a date is February 29 (leap day)."""
    return date.month == 2 and date.day == 29

def is_leap_year(year):
    """Check if the given year is a leap year."""
    return calendar.isleap(year)

def calculate_weeks_needed(year, start_date=None):
    """Calculate the number of weeks needed to reach December 31st."""
    if start_date is None:
        # Find the Monday on or before January 1
        jan1 = datetime.date(year, 1, 1)
        day_of_week = jan1.weekday()  # 0 for Monday, 6 for Sunday
        start_date = jan1 - datetime.timedelta(days=day_of_week)
    
    # Find December 31st
    dec31 = datetime.date(year, 12, 31)
    
    # Calculate days from start to December 31st
    days_diff = (dec31 - start_date).days
    
    # Calculate weeks needed (add 1 to include the final week)
    weeks_needed = (days_diff // 7) + 1
    
    return weeks_needed

def create_circular_calendar(year=2025, start_date=None, current_date=None, figsize=(14,14)):
    # If no start_date provided, use Monday on or before January 1st
    if start_date is None:
        jan1 = datetime.date(year, 1, 1)
        day_of_week = jan1.weekday()  # 0 for Monday, 6 for Sunday
        start_date = jan1 - datetime.timedelta(days=day_of_week)
    
    # If no current_date provided, use today's date in US Central timezone
    if current_date is None:
        current_date = get_today_central()
    
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
    
    # Calculate total weeks needed to include December 31st
    total_weeks = calculate_weeks_needed(year, start_date)
    
    # Force end date to be December 31st
    end_date = datetime.date(year, 12, 31)
    
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
            # Calculate the actual date for this calendar position
            day_date = week_start_date + datetime.timedelta(days=day_idx)
            
            # Skip if we're past December 31st
            if day_date.year > year:
                continue
                
            # Track traditional month boundaries
            if day_date.month != current_month:
                current_month = day_date.month
                calendar_day = week_idx * 7 + day_idx
                traditional_months.append((day_date.strftime('%b'), calendar_day))
            
            # Calculate radius for this day (Sunday innermost, Monday outermost)
            day_outer_radius = outer_radius - day_idx * day_radius_width
            day_inner_radius = day_outer_radius - day_radius_width
            
            # Determine color based on date
            # Special handling for leap day
            if is_leap_day(day_date):
                # For leap day, use a special color or pattern
                if day_date == current_date:  # If today is leap day
                    color = '#AAFFAA'  # Light green for leap day (lighter than completed)
                else:
                    color = '#004400'  # Darker green for leap day (darker than background)
            else:
                # Normal day coloring
                if day_date < current_date:
                    color = completed_color  # Past day (green)
                elif day_date == current_date:
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
            # For the last month, use the next year's first month
            next_angle = 90 - total_weeks * angle_per_week
        
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
    
    # Calculate how many full 13-month periods we have
    full_13_months = total_weeks // 4
    
    # Add 13-month calendar month labels - ALWAYS HORIZONTAL
    for month_idx in range(full_13_months):
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
    
    # Handle any remaining weeks (past the last full 13-month)
    remaining_weeks = total_weeks % 4
    if remaining_weeks > 0:
        # Add a label for the extra month
        month_start_week = full_13_months * 4
        month_end_week = total_weeks
        
        # Calculate angles for this partial month
        month_start_angle = 90 - month_start_week * angle_per_week
        month_end_angle = 90 - month_end_week * angle_per_week
        if month_start_angle < month_end_angle:
            month_start_angle += 360
            
        month_mid_angle = (month_start_angle + month_end_angle) / 2
        
        # Add month label
        mid_radius = (inner_radius + outer_radius) / 2
        month_x = mid_radius * np.cos(np.radians(month_mid_angle))
        month_y = mid_radius * np.sin(np.radians(month_mid_angle))
            
        ax.text(month_x, month_y, f"M{full_13_months+1}", color=month_label_color, 
               ha='center', va='center', fontsize=12, fontweight='bold',
               rotation=0)
        
        # Draw line at the start of this extra month
        boundary_angle = 90 - month_start_week * angle_per_week
        x1 = inner_radius * np.cos(np.radians(boundary_angle))
        y1 = inner_radius * np.sin(np.radians(boundary_angle))
        x2 = outer_radius * np.cos(np.radians(boundary_angle))
        y2 = outer_radius * np.sin(np.radians(boundary_angle))
        ax.plot([x1, x2], [y1, y2], color='#00CC00', linestyle='-', linewidth=1)
    
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
    if is_leap_day(current_date):
        ax.text(-outer_radius-2.5, -outer_radius-2.5, 
                f"TODAY: {date_str}\nToday is a Leap Day! Take today to rest & rejuvenate!", 
                color='#00FF00', fontsize=10, family='monospace')
    else:
        ax.text(-outer_radius-2.5, -outer_radius-2.5, f"TODAY: {date_str}", 
                color='#00FF00', fontsize=10, family='monospace')
    
    # Add start date and end date indicators in opposite corner
    start_date_str = start_date.strftime("%Y-%m-%d")
    end_date_str = end_date.strftime("%Y-%m-%d")
    ax.text(outer_radius-2.5, -outer_radius-2.5, 
            f"START: {start_date_str}\nEND: {end_date_str}\nWEEKS: {total_weeks}", 
            color='#00FF00', fontsize=10, family='monospace', ha='right')
    
    plt.tight_layout()
    
    return fig

def monday_closest_to_jan1(current_year=None):
    # Get current year
    if current_year == None:
        current_year = get_today_central().year
    
    # Create date object for January 1st of current year
    jan1 = datetime.date(current_year, 1, 1)
    
    # Get the day of the week (0 is Monday, 6 is Sunday)
    day_of_week = jan1.weekday()
    
    # Calculate days to nearest Monday on or before Jan 1
    if day_of_week == 0:  # If Jan 1 is already Monday
        return jan1
    else:  # For any other day, go backward to previous Monday
        return jan1 - datetime.timedelta(days=day_of_week)

# Streamlit app
st.set_page_config(page_title="The Dalendar", layout="wide")
st.title(f"{datetime.datetime.now().year} Dalendar")

# Add some interactive controls
_, col2, _ = st.columns([1, 3, 1])

# Create the calendar
today = get_today_central()
fig = create_circular_calendar(year=today.year, start_date=monday_closest_to_jan1(today.year), current_date=today, figsize=(12,12))

# Display the calendar
with col2:
    st.pyplot(fig, use_container_width=True)

# Add explanation
st.markdown("""
## About This Calendar
- **Dalendar** = Dan's Calendar
- **Green sections**: Completed days
- **White section**: Current day
""")