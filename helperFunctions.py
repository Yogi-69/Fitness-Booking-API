import json
import os
from datetime import datetime
import pytz

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

def convertToTimezone(dateTimeStr, targetTzStr):
    try:
        dt = datetime.fromisoformat(dateTimeStr)        
        ist_tz = pytz.timezone("Asia/Kolkata")
        if dt.tzinfo is None:
            dt_ist = ist_tz.localize(dt)
        else:
            dt_ist = dt.astimezone(ist_tz)
        
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
