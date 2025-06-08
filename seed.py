import json
import os
from datetime import datetime, timedelta
import pytz

dataDir = "data"
os.makedirs(dataDir, exist_ok=True)
classesFile = os.path.join(dataDir, "classes.json")
bookingsFile = os.path.join(dataDir, "bookings.json")

ist = pytz.timezone("Asia/Kolkata")


def getClassDatetime(daysFromNow: int, hour: int, minute: int = 0) -> str:
    """
    Generate an ISO-formatted IST datetime string n days from now.
    """
    now = datetime.now(ist)
    classTime = (now + timedelta(days=daysFromNow)).replace(
        hour=hour, minute=minute, second=0, microsecond=0
    )
    return classTime.isoformat()


def createClass(classId: int, name: str, instructor: str, dateTime: str, availableSlots: int) -> dict:
    """
    Creates a single class dictionary in the expected format.
    """
    return {
        "id": classId,
        "class": name,
        "instructor": instructor,
        "dateTime": dateTime,
        "availableSlots": availableSlots
    }


def seedData():
    classes = [
        createClass(
            classId=1,
            name="Yoga",
            instructor="Aditya Sharma",
            dateTime=getClassDatetime(daysFromNow=0, hour=7),
            availableSlots=5
        ),
        createClass(
            classId=2,
            name="Zumba",
            instructor="Rahul Verma",
            dateTime=getClassDatetime(daysFromNow=1, hour=18),
            availableSlots=10
        ),
        createClass(
            classId=3,
            name="HIIT - High Intensity Interval Training",
            instructor="Priya Singh",
            dateTime=getClassDatetime(daysFromNow=2, hour=6, minute=30),
            availableSlots=8
        )
    ]

    with open(classesFile, "w") as f:
        json.dump(classes, f, indent=4)

    with open(bookingsFile, "w") as f:
        json.dump([], f, indent=4)

    print("✅ Seeding complete. Sample classes added.")


if __name__ == "__main__":
    seedData()