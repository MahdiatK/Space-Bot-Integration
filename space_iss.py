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

import requests
import json
import time
from iso3166 import countries

# 2. Complete the if statement to ask the user for the Webex access token.
choice = input("Do you want to use the hard-coded Webex token? (y/n): ")

if choice.lower() == "n":
    token_input = input("Please enter your Webex access token: ")
    accessToken = f"Bearer {token_input}"
else:
    accessToken = "Bearer YOUR_WEBEX_TOKEN_HERE"

# 3. Provide the URL to the Webex room API.

rooms_url = "https://webexapis.com/v1/rooms"
r = requests.get(rooms_url, headers={"Authorization": accessToken})

#######################################################################################
# DO NOT EDIT ANY BLOCKS WITH r.status_code
if r.status_code != 200:
    raise Exception(f"Webex API error: {r.status_code} - {r.text}")
#######################################################################################

# 4. Create a loop to print the type and title of each room.
print("\nList of your Webex rooms:")
rooms = r.json()["items"]
for room in rooms:
    print(f"Type: {room['type']} | Name: {room['title']}")

#######################################################################################
# SEARCH FOR WEBEX ROOM TO MONITOR
#  - Searches for user-supplied room name.
#  - If found, print "found" message, else prints error.
#  - Stores values for later use by bot.
# DO NOT EDIT CODE IN THIS BLOCK
#######################################################################################

while True:
    roomSearch = input("\nWhich room should the bot monitor for /seconds messages? ")
    roomIdToGetMessages = None
    
    for room in rooms:
        if(room["title"].find(roomNameToSearch) != -1):
            print ("Found rooms with the word " + roomNameToSearch)
            print(room["title"])
            roomIdToGetMessages = room["id"]
            roomTitleToGetMessages = room["title"]
            print("Found room: " + roomTitleToGetMessages)
            break

    if not roomIdToGetMessages:
        print("No matching room found, please try again.")
    else:
        print(f"Monitoring room: {roomTitleToGetMessages}")
        break  
######################################################################################
# WEBEX BOT CODE
#  Starts Webex bot to listen for and respond to /seconds messages.
######################################################################################

while True:
    time.sleep(1)
    params = {"roomId": roomIdToGetMessages, "max": 1}
 
# 5. Provide the URL to the Webex messages API.    
    msg_resp = requests.get("https://webexapis.com/v1/messages",
                            params=params,
                            headers={"Authorization": accessToken})
 
    # verify if the retuned HTTP status code is 200/OK
if msg_resp.status_code != 200:
        print(f"Message API error: {msg_resp.status_code}")
        continue
        raise Exception( "Incorrect reply from Webex API. Status code: {}. Text: {}".format(r.status_code, r.text))

    msg_data = msg_resp.json()
    if len(msg_data["items"]) == 0:
        continue
    
    message = msg_data["items"][0]["text"]
    print("Received message:", message)
    
    if message.startswith("/") and message[1:].isdigit():
        seconds = int(message[1:])
         if seconds > 5:
            seconds = 5
        else:
          print(f"Waiting {seconds} seconds before fetching ISS data...")
          time.sleep(seconds
            
     time.sleep(seconds)     
    
# 6. Provide the URL to the ISS Current Location API.         
        iss_resp = requests.get("http://api.open-notify.org/iss-now.json")
        if iss_resp.status_code != 200:
            print("Could not get ISS data.")
            continue

# 7. Record the ISS GPS coordinates and timestamp.

        iss_json = iss_resp.json()
        lat = iss_json["iss_position"]["latitude"]
        lon = iss_json["iss_position"]["longitude"]
        timestamp = iss_json["timestamp"]
        
# 8. Convert the timestamp epoch value to a human readable date and time.
        # Use the time.ctime function to convert the timestamp to a human readable date and time.
    timeString = time.ctime(timestamp)   
   
# 9. Provide your Geoloaction API consumer key.
    
       geo_params = {
            "key": "YOUR_LOCATIONIQ_KEY",
            "lat": lat,
            "lon": lon,
            "format": "json"
        }

# 10. Provide the URL to the Reverse GeoCode API.
    # Get location information using the API reverse geocode service using the HTTP GET method
        geo_resp = requests.get("https://us1.locationiq.com/v1/reverse",
                                params=geo_params)
                        )

    # Verify if the returned JSON data from the API service are OK
        geo_json = geo_resp.json()
        
        geo_resp = requests.get("https://us1.locationiq.com/v1/reverse",
                                params=geo_params)
        if geo_resp.status_code != 200:
            print("Error retrieving location data.")
            continue

# 11. Store the location received from the API in a required variables
        address = geo_json.get("address", {})
        country = address.get("country", "Unknown")
        state = address.get("state", "")
        city = address.get("city", "")
        road = address.get("road", "")

# 12. Complete the code to format the response message.
#     Example responseMessage result: In Austin, Texas the ISS will fly over on Thu Jun 18 18:42:36 2020 for 242 seconds.
        #responseMessage = "On {}, the ISS was flying over the following location: \n{} \n{}, {} \n{}\n({}\", {}\")".format(timeString, StreetResult, CityResult, StateResult, CountryResult, lat, lng)

if country == "Unknown":
            responseMessage = f"On {timeString}, the ISS was flying over the ocean at ({lat}°, {lon}°)."
        elif city:
            responseMessage = f"On {timeString}, the ISS was flying over {city}, {country}. ({lat}°, {lon}°)"
        elif state:
            responseMessage = f"On {timeString}, the ISS was above {state}, {country}. ({lat}°, {lon}°)"
        else:
            responseMessage = f"On {timeString}, the ISS was flying over {country}. ({lat}°, {lon}°)"

        print("Sending to Webex:", responseMessage)

# 13. Complete the code to post the message to the Webex room.         
        # the Webex HTTP headers, including the Authoriztion and Content-Type
 headers = {
            "Authorization": accessToken,
            "Content-Type": "application/json"
        }
        post_data = {
            "roomId": roomIdToGetMessages,
            "text": responseMessage
        }
        # Post the call to the Webex message API.
 send_resp = requests.post("https://webexapis.com/v1/messages", 
                              data = json.dumps(<!!!REPLACEME!!!>), 
                              headers = <!!!REPLACEME!!!>
                         )
        <!!!REPLACEME with code for error handling in case request not successfull>
                







