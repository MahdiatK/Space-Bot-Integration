###############################################################
#This is just a starter code for the assignment 1, 
# you need to follow the assignment brief to complete all the tasks required by the assessemnt brief
#
#  This program:
# - Asks the user to enter an access token or use the hard coded access token.
# - Lists the user's Webex rooms.
# - Asks the user which Webex room to monitor for "/seconds" of requests.
# - Monitors the selected Webex Team room every second for "/seconds" messages.
# - Discovers GPS coordinates of the ISS flyover using ISS API.
# - Display the geographical location using geolocation API based on the GPS coordinates.
# - Formats and sends the results back to the Webex Team room.
#
# The student will:
# 1. Import libraries for API requests, JSON formatting, epoch time conversion, and iso3166.
# 2. Complete the if statement to ask the user for the Webex access token.
# 3. Provide the URL to the Webex room API.
# 4. Create a loop to print the type and title of each room.
# 5. Provide the URL to the Webex messages API.
# 6. Provide the URL to the ISS Current Location API.
# 7. Record the ISS GPS coordinates and timestamp.
# 8. Convert the timestamp epoch value to a human readable date and time.
# 9. Provide your Geoloaction API consumer key.
# 10. Provide the URL to the Geoloaction address API.
# 11. Store the location received from the Geoloaction API in a variable.
# 12. Complete the code to format the response message.
# 13. Complete the code to post the message to the Webex room.
###############################################################
 
# 1. Import libraries for API requests, JSON formatting, epoch time conversion, and iso3166.

# 1. Import libraries for API requests, JSON formatting, epoch time conversion, and iso3166.
import requests
import json
import time
from iso3166 import countries

# 2. Ask the user for the Webex access token.
choice = input("Do you wish to use the hard-coded Webex token? (y/n): ")

if choice.lower() == "n":
    token_input = input("Please enter your Webex access token: ")
    accessToken = f"Bearer {token_input}"
else:
    accessToken = "Bearer NzU4YzIzODctOWZiNi00NTRiLWFjYjYtZjI4YTJhOGZmOTUwYzQxM2ZhZmYtOTM2_P0A1_bdd2aed2-da17-481d-bd6f-b43037ee90b7"

# 3. Provide the URL to the Webex room API.
r = requests.get("https://webexapis.com/v1/rooms",
                 headers={"Authorization": accessToken})

#######################################################################################
# DO NOT EDIT ANY BLOCKS WITH r.status_code
if not r.status_code == 200:
    raise Exception(f"Incorrect reply from Webex API. Status code: {r.status_code}. Text: {r.text}")
#######################################################################################

# 4. Print the type and title of each room.
print("\nList of available rooms:")
rooms = r.json()["items"]
for room in rooms:
    print(f"Type: {room['type']} | Title: {room['title']}")

#######################################################################################
# SEARCH FOR WEBEX ROOM TO MONITOR
#######################################################################################
while True:
    roomNameToSearch = input("\nWhich room should be monitored for /seconds messages? ")
    roomIdToGetMessages = None

    for room in rooms:
        if roomNameToSearch.lower() in room["title"].lower():
            print(f"Found room with the word '{roomNameToSearch}': {room['title']}")
            roomIdToGetMessages = room["id"]
            roomTitleToGetMessages = room["title"]
            print("Found room:", roomTitleToGetMessages)
            break

    if roomIdToGetMessages is None:
        print("Sorry, I didn’t find any room with that name. Please try again.")
    else:
        print("Monitoring room:", roomTitleToGetMessages)
        break

######################################################################################
# WEBEX BOT CODE
#  Starts Webex bot to listen for and respond to /seconds messages.
######################################################################################

while True:
    time.sleep(1)
    GetParameters = {
        "roomId": roomIdToGetMessages,
        "max": 1
    }

# 5. Provide the URL to the Webex messages API.
    r = requests.get("https://webexapis.com/v1/messages",
                     params=GetParameters,
                     headers={"Authorization": accessToken})

    # verify if the returned HTTP status code is 200/OK
    if not r.status_code == 200:
        print(f"Incorrect reply from Webex API. Status code: {r.status_code}. Text: {r.text}")
        continue

    json_data = r.json()
    if len(json_data["items"]) == 0:
        continue

    messages = json_data["items"]
    message = messages[0]["text"]
    print("Received message:", message)

    # check for a command like /5 or /3
    if message.startswith("/") and message[1:].isdigit():
        seconds = int(message[1:])
        if seconds > 5:
            seconds = 5

        print(f"Waiting {seconds} seconds before checking ISS location...")
        time.sleep(seconds)

# 6. Provide the URL to the ISS Current Location API.
        iss_response = requests.get("http://api.open-notify.org/iss-now.json")
        if iss_response.status_code != 200:
            print("Error retrieving ISS data.")
            continue

        iss_json = iss_response.json()

# 7. Record the ISS GPS coordinates and timestamp.
        lat = iss_json["iss_position"]["latitude"]
        lon = iss_json["iss_position"]["longitude"]
        timestamp = iss_json["timestamp"]

# 8. Convert the epoch time to a readable date/time.
        timeString = time.ctime(timestamp)

# 9. Provide your Geolocation API consumer key.
        geo_params = {
            "key": "pk.3ab1a8e82167c509f5f2a88e29533799",
            "lat": lat,
            "lon": lon,
            "format": "json"
        }

# 10. Provide the URL to the Reverse GeoCode API.
        geo_response = requests.get("https://us1.locationiq.com/v1/reverse",
                                    params=geo_params)

        if geo_response.status_code != 200:
            print("Error retrieving geolocation data.")
            continue

        geo_json = geo_response.json()

# 11. Store the location received from the API.
        address = geo_json.get("address", {})
        country = address.get("country", "Unknown")
        state = address.get("state", "")
        city = address.get("city", "")
        road = address.get("road", "")

# 12. Format the response message.
        if country == "Unknown":
            responseMessage = f"On {timeString}, the ISS was flying over the ocean at ({lat}°, {lon}°)."
        elif city:
            responseMessage = f"On {timeString}, the ISS was flying over {city}, {country}. ({lat}°, {lon}°)"
        elif state:
            responseMessage = f"On {timeString}, the ISS was above {state}, {country}. ({lat}°, {lon}°)"
        else:
            responseMessage = f"On {timeString}, the ISS was flying over {country}. ({lat}°, {lon}°)"

        print("Sending to Webex:", responseMessage)

# 13. Post the message to the Webex room.
        HTTPHeaders = {
            "Authorization": accessToken,
            "Content-Type": "application/json"
        }
        PostData = {
            "roomId": roomIdToGetMessages,
            "text": responseMessage
        }

        send_response = requests.post("https://webexapis.com/v1/messages",
                                      data=json.dumps(PostData),
                                      headers=HTTPHeaders)

        if send_response.status_code != 200:
            print("Failed to send message:", send_response.text)
        else:
            print("Message sent successfully!\n")

    else:
     
        continue
