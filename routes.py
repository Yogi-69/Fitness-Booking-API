from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, EmailStr
from helperFunctions import (
    loadClassesData, loadBookingsData,
    saveClassesData, saveBookingsData,
    convertToTimezone, getRelativeDay
)
import pytz 
from datetime import datetime

router = APIRouter()

class BookingRequest(BaseModel):
    classId: int
    clientName: str
    clientEmail: EmailStr

@router.get("/")
def connectionCheck():
    return {"message": "Fitness Booking API is running."}

@router.get("/classes")
def getClasses(timezone: str = None):
    try:
        classes = loadClassesData()
        if not classes:
            return {"message": "No classes available."}
        
        useTimezoneConversion = timezone is not None and timezone != "Asia/Kolkata"
        
        if useTimezoneConversion:
            try:
                targetTimezone = pytz.timezone(timezone)
                currentDate = datetime.now(targetTimezone)
            except pytz.exceptions.UnknownTimeZoneError:
                raise HTTPException(status_code=400, detail=f"Invalid timezone: {timezone}")
        else:
            currentDate = datetime.now(pytz.timezone("Asia/Kolkata"))
        
        result = []
        
        for classItem in classes:
            if useTimezoneConversion:
                convertedDateTime = convertToTimezone(classItem["dateTime"], timezone)
                date = datetime.fromisoformat(convertedDateTime.replace('Z', ''))
                
                if date.tzinfo is None:
                    date = targetTimezone.localize(date)
                
                timezoneAbvr = date.strftime("%Z") or timezone.split('/')[-1]
                timezoneDisplay = timezoneAbvr
            else:
                date = datetime.fromisoformat(classItem["dateTime"])
                ist_tz = pytz.timezone("Asia/Kolkata")
                if date.tzinfo is None:
                    date = ist_tz.localize(date)
                timezoneDisplay = "IST"
            
            timeStr = date.strftime("%I:%M %p").lstrip("0").replace(":00", "")
            relativeDay = getRelativeDay(date, currentDate)
            
            formattedClass = {
                "id": classItem["id"],
                "class": classItem["class"],
                "instructor": classItem["instructor"],
                "dateTime": f"Class scheduled for {relativeDay} at {timeStr} {timezoneDisplay}",
                "availableSlots": classItem["availableSlots"]
            }
            
            if useTimezoneConversion:
                formattedClass["originalIST"] = classItem["dateTime"]
                formattedClass["convertedTimezone"] = timezone
            
            result.append(formattedClass)
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error loading classes: {str(e)}")

@router.post("/book")
def bookClass(booking: BookingRequest):
    try:
        classes = loadClassesData()
        bookings = loadBookingsData()

        matchedClass = next((cls for cls in classes if cls["id"] == booking.classId), None)

        if not matchedClass:
            raise HTTPException(status_code=404, detail="Class not found.")

        if matchedClass["availableSlots"] <= 0:
            raise HTTPException(status_code=400, detail="No slots available.")

        existing_booking = next((b for b in bookings 
                               if b["classId"] == booking.classId and 
                                  b["clientEmail"] == booking.clientEmail), None)
        
        if existing_booking:
            raise HTTPException(status_code=400, detail="You have already booked this class.")

        matchedClass["availableSlots"] -= 1
        saveClassesData(classes)

        newBooking = {
            "classId": booking.classId,
            "className": matchedClass["class"],
            "instructor": matchedClass["instructor"],
            "dateTime": matchedClass["dateTime"],
            "clientName": booking.clientName,
            "clientEmail": booking.clientEmail
        }
        bookings.append(newBooking)
        saveBookingsData(bookings)

        dt = datetime.fromisoformat(matchedClass["dateTime"])
        ist_tz = pytz.timezone("Asia/Kolkata")
        dt_ist = ist_tz.localize(dt) if dt.tzinfo is None else dt
        readableTime = dt_ist.strftime("%I:%M %p IST").lstrip("0")

        return {
            "message": f"🎉 Great choice, {booking.clientName}! Your spot in {matchedClass['class']} is reserved for {readableTime}.",
            "bookingDetails": {
                "classId": booking.classId,
                "className": matchedClass["class"],
                "instructor": matchedClass["instructor"],
                "dateTime": readableTime,
                "clientName": booking.clientName,
                "clientEmail": booking.clientEmail,
                "remainingSlots": matchedClass["availableSlots"]
            }
        }
        
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Booking failed: {str(e)}")

@router.get("/bookings")
def getBookingsByEmail(email: EmailStr):
    try:
        bookings = loadBookingsData()
        userBookings = [b for b in bookings if b["clientEmail"].lower() == email.lower()]
        if not userBookings:
            return {"message": "No bookings found for this email."}
        return userBookings
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving bookings: {str(e)}")
