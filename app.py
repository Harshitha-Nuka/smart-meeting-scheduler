import calendar
from datetime import datetime, timedelta


WORKING_HOURS = (9, 17)  # 9 AM - 5 PM
HOLIDAYS = [(2025, 1, 1), (2025, 12, 25)]  


meetings = {}

def is_working_day(date):
    """Check if the given date is a working day."""
    if date.weekday() >= 5:  # 5 = Saturday, 6 = Sunday
        return False
    if (date.year, date.month, date.day) in HOLIDAYS:
        return False
    return True

def get_available_slots(user, date):
    """Return available time slots for a user on a given date."""
    if not is_working_day(date):
        return []
    
    booked_slots = meetings.get(user, [])
    available_slots = []
    current_time = datetime(date.year, date.month, date.day, WORKING_HOURS[0], 0)
    end_time = datetime(date.year, date.month, date.day, WORKING_HOURS[1], 0)
    
    while current_time < end_time:
        slot = (current_time, current_time + timedelta(hours=1))
        if all(not (slot[0] < b_end and slot[1] > b_start) for b_start, b_end in booked_slots):
            available_slots.append(slot)
        current_time += timedelta(hours=1)
    
    return available_slots

def schedule_meeting(user, date, start_hour):
    """Schedule a meeting for a user on a given date and time."""
    if not is_working_day(date):
        return "Cannot schedule on weekends or holidays."
    
    start_time = datetime(date.year, date.month, date.day, start_hour, 0)
    end_time = start_time + timedelta(hours=1)
    
    if start_hour < WORKING_HOURS[0] or start_hour >= WORKING_HOURS[1]:
        return "Meeting time outside working hours."
    
    user_meetings = meetings.setdefault(user, [])
    
    if any(start_time < b_end and end_time > b_start for b_start, b_end in user_meetings):
        return "Time slot not available."
    
    user_meetings.append((start_time, end_time))
    return f"Meeting scheduled for {user} on {date.strftime('%Y-%m-%d')} from {start_hour}:00 to {start_hour+1}:00."

def view_meetings(user):
    """View upcoming meetings for a user."""
    return meetings.get(user, [])

# Example usage
date = datetime(2025, 3, 17)
print(schedule_meeting("Alice", date, 10))
print(get_available_slots("Alice", date))
print(view_meetings("Alice"))

