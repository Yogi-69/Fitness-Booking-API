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

## 📌 API Endpoints

### 1. `GET /classes`

Returns a list of all upcoming fitness classes.

**Query Parameters (optional):**
- `tz`: Timezone string (e.g., `Asia/Kolkata`, `UTC`, `America/New_York`)

**Example:**
GET /classes?tz=America/New_York


---

### 2. `POST /book`

Book a spot in a class.

**Request Body:**
`json`
{
  "name": "Jane Doe",
  "email": "jane@example.com",
  "class_id": "hiit_001"
}
Responses:

200 OK: Booking successful
400 Bad Request: Invalid class ID or email format
3. GET /bookings
Fetch all bookings for a given user.

Query Parameters:

email: User email
Example:

GET /bookings?email=jane@example.com
