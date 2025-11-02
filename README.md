# Space-Bot-Integration

# 🚀 Space Bot API Investigation Sheet

**Total Marks: 30**  
**Part 1: Collect Required API Documentation**

This investigation sheet helps you gather key technical information from the three APIs required for the Space Bot project: **Webex Messaging API**, **ISS Current Location API**, and a **Geocoding API** (LocationIQ or Mapbox or other), plus the Python time module.

---

## ✅ Section 1: Webex Messaging API (7 marks)

| Criteria | Details |
|---------|---------|
| API Base URL | `(https://webexapis.com/v1/)` |
| Authentication Method | `OAuth 2.0 Access Token` |
| Endpoint to list rooms | `GET /rooms` |
| Endpoint to get messages | `GET /messages?roomId={roomId}` |
| Endpoint to send message | `POST /messages` |
| Required headers | `{ "Authorization": "Bearer <ACCESS_TOKEN>", "Content-Type": "application/json" }` |
| Sample full GET or POST request | ````python` |

---

## 🛰️ Section 2: ISS Current Location API (3 marks)

| Criteria | Details |
|---------|---------|
| API Base URL | `http://api.open-notify.org/` |
| Endpoint for current ISS location | `GET /iss-now.json` |
| Sample response format (example JSON) |  
```json
{
  "timestamp": 1730568000,
  "message": "success",
  "iss_position": {
    "latitude": "51.0",
    "longitude": "-0.1"
  }
}
```
|

---

## 🗺️ Section 3: Geocoding API (LocationIQ or Mapbox or other) (6 marks)

| Criteria | Details |
|---------|---------|
| Provider used (circle one) | LocationIQ - Best free plan and easiest to set up |
| API Base URL | `(https://us1.locationiq.com/v1/)` |
| Endpoint for reverse geocoding | `GET /reverse` |
| Authentication method | `API Key` |
| Required query parameters | `key`, `lat`, `lon`, `format=json` |
| Sample request with latitude/longitude | `(https://us1.locationiq.com/v1/reverse?key=YOUR_API_KEY&lat=51.0&lon=-0.1&format=json)` |
| Sample JSON response (formatted example) |  
```json
{
  "place_id": "123456",
  "lat": "51.0",
  "lon": "-0.1",
  "display_name": "London, England, United Kingdom",
  "address": {
    "city": "London",
    "country": "United Kingdom"
  }
}

```
|

---

## ⏰ Section 4: Epoch to Human Time Conversion (Python time module) (2 marks)

| Criteria | Details |
|---------|---------|
| Library used | `time` |
| Function used to convert epoch | `time.strftime()` with `time.localtime()` |
| Sample code to convert timestamp |  
```python
import time
epoch_time = 1730568000
local_time = time.localtime(epoch_time)
print(time.strftime("%Y/%m/%d %I:%M:%S %p", local_time))  
```
|
| Output (human-readable time) | `2025-11-02 22:00:00` |

---

## 🧩 Section 5: Web Architecture & MVC Design Pattern (12 marks)

### 🌐 Web Architecture – Client-Server Model

- **Client**: | Space Bot Python script (and user through Webex)
- **Server**: external APIs (Webex Cloud, ISS API Server, and LocationIQ Server) that help provide data
- Client sends a HTTP request to one of the API servers which thne return a JSON response

### 🔁 RESTful API Usage

- POST for sending messages back to Webex
- GET for retrieving rooms and ISS location

### 🧠 MVC Pattern in Space Bot

| Component   | Description |
|------------|-------------|
| **Model**  |  | Retrieves ISS location from the ISS api and transcribing the coordinates through LocationIQ, handles API and data |
| **View**   |  | The display render, so the webex chat room interface and messages |
| **Controller** |  | The main Python script (space_iss.py) |


#### Example:
- Model: ISS + LocationIQ APIs
- View: Webex room messages
- Controller: Python logic

---

### 📝 Notes

- Use official documentation for accuracy (e.g. developer.webex.com, locationiq.com or Mapbox, open-notify.org or other ISS API).
- Be prepared to explain your findings to your instructor or demo how you retrieved them using tools like Postman, Curl, or Python scripts.

---

### ✅ Total: /30
