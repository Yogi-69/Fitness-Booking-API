# 🧘‍♀️ Fitness Booking API 🏋️‍♂️

A simple yet functional Fitness Booking API built using **FastAPI** — designed to simulate a real-world backend for scheduling fitness classes like **Yoga**, **Zumba**, and **HIIT**. Built with ease-of-use, timezone support, and clean error handling in mind. 💪

---

## 🚀 Features

- 📅 **View Upcoming Classes** — List all scheduled fitness classes.
- 📝 **Book Your Spot** — Reserve a class using your name, email, and class ID.
- 🔍 **Check Your Bookings** — Retrieve bookings by email.
- 🕒 **Timezone Support** — Convert timings from IST to your local timezone.
- ✅ **Custom Validation Errors** — Cleaner and more informative error messages.

---

## 🛠️ Project Structure

```
.
├── data
│   ├── classes.json
│   ├── bookings.json
├── main.py
├── seed.py
├── routes.py
└── helperFunctions.py
```


---

## 📌 API Endpoints

### 1. `GET /classes`

Returns a list of all upcoming fitness classes.

**Query Parameters (optional):**
- `timezone`: Timezone string (e.g., `Asia/Kolkata`, `UTC`, `America/New_York`)

**Example:**

GET /classes?timezone=America/New_York


### 2. `POST /book`

Book a spot in a class.

**Request Body:**

`json`
```
{
  "class_id": 1,
  "name": "Jane Doe",
  "email": "jane@example.com",
}
```


### 3. 'GET /bookings'

Fetch all bookings for a given user.

**Query Parameters:**

`email`: User email

**Example:**

GET /bookings?email=jane@example.com


---

## 🧪 Data Seeding

Run the following command to generate mock class data:

```bash
python seed.py
```

This creates a classes.json and the bookings.json file populated with scheduled classes and instructor info.


---

## 🔧 Tech Stack

Python 3.10+

`FastAPI` — Web framework for high performance APIs

`Pydantic` — Data validation and settings management

`Uvicorn` — ASGI server for running FastAPI apps


---

## 🌍 Timezone Handling

The API supports optional timezone conversion for class listings. Internally, all class times are stored in `IST (Indian Standard Time)` and can be converted on-the-fly to the user’s local timezone via the `timezone` query parameter.

Helper utilities also provide human-friendly formatting like:
```
today
tomorrow
in 3 days
```

---

## ⚠️ Error Handling

**Custom validation ensures:**

Clean and structured error messages
Clear feedback for invalid emails or booking issues


---

## 🧑‍💻 Getting Started

**Clone the repo:**

```bash
git clone https://github.com/yourusername/fitness-booking-api.git
cd fitness-booking-api
```

**Install dependencies:**

```bash
pip install -r requirements.txt
```

**Seed mock data:**

```bash
python seed.py
```

**Run the app:**

```bash
uvicorn main:app --reload
```


---

## :cherry_blossom: General Usage

**📆 1. Get Available Classes**

- Without `timezone`

```bash
curl http://127.0.0.1:8000/classes
```

- With `timezone` `(e.g. America/New_York)`
  
```bash
curl "http://127.0.0.1:8000/classes?timezone=America/New_York"
```

**📝 2. Book a Class**

Replace values as needed `(classId, clientName, clientEmail)`

```bash
curl -X POST http://127.0.0.1:8000/book \
  -H "Content-Type: application/json" \
  -d '{
        "classId": 1,
        "clientName": "John Doe",
        "clientEmail": "john@example.com"
      }'
```

**📩 3. Get Bookings by Email**

Replace the `email` with the one used in booking

```bash
curl "http://127.0.0.1:8000/bookings?email=john@example.com"
```


---
