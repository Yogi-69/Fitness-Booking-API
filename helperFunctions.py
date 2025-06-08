import json
import os
from datetime import datetime
import pytz  # back to using pytz

dataDir = "data"
classesFile = os.path.join(dataDir, "classes.json")
bookingsFile = os.path.join(dataDir, "bookings.json")

def loadClassesData():
    try:
        if not os.path.exists(classesFile):
            return []
        with open(classesFile, "r") as file:
            return json.load(file)
    except Exception as e:
        raise Exception(f"Failed to load classes: {str(e)}")

def saveClassesData(classes):
    try:
        with open(classesFile, "w") as file:
            json.dump(classes, file, indent=4)
    except Exception as e:
        raise Exception(f"Failed to save classes: {str(e)}")

def loadBookingsData():
    try:
        if not os.path.exists(bookingsFile):
            return []
        with open(bookingsFile, "r") as file:
            return json.load(file)
    except Exception as e:
        raise Exception(f"Failed to load bookings: {str(e)}")

def saveBookingsData(bookings):
    try:
        with open(bookingsFile, "w") as file:
            json.dump(bookings, file, indent=4)
    except Exception as e:
        raise Exception(f"Failed to save bookings: {str(e)}")

# def convertToTimezone(dateTimeStr, targetTzStr):
#     try:
#         dt = datetime.fromisoformat(dateTimeStr)
#         utc = pytz.utc
#         dt = dt.replace(tzinfo=utc) if dt.tzinfo is None else dt.astimezone(utc)
#         targetTz = pytz.timezone(targetTzStr)
#         return dt.astimezone(targetTz).isoformat()
#     except Exception as e:
#         raise Exception(f"Failed to convert timezone: {str(e)}")
def convertToTimezone(dateTimeStr, targetTzStr):
    """
    Convert datetime from IST (stored format) to target timezone
    
    Args:
        dateTimeStr: DateTime string in IST format (e.g., "2024-12-10T09:00:00")
        targetTzStr: Target timezone string (e.g., "America/New_York")
    
    Returns:
        ISO formatted datetime string in target timezone
    """
    try:
        # Parse the datetime (assume it's in IST as stored)
        dt = datetime.fromisoformat(dateTimeStr)
        
        # Set as IST timezone (since classes are created in IST)
        ist_tz = pytz.timezone("Asia/Kolkata")
        if dt.tzinfo is None:
            dt_ist = ist_tz.localize(dt)
        else:
            dt_ist = dt.astimezone(ist_tz)
        
        # Convert to target timezone
        target_tz = pytz.timezone(targetTzStr)
        dt_target = dt_ist.astimezone(target_tz)
        
        return dt_target.isoformat()
        
    except Exception as e:
        raise Exception(f"Failed to convert timezone: {str(e)}")

def getRelativeDay(dt: datetime, currentDate: datetime) -> str:
    """Determine if the date is today, tomorrow, or in X days."""
    delta = (dt.date() - currentDate.date()).days
    if delta == 0:
        return "today"
    elif delta == 1:
        return "tomorrow"
    else:
        return f"in {delta} days"