import requests
import datetime
import time

def sectomin(seconds):
    return seconds//60

API_KEY = 'AIzaSyCkyvmRaEWLvpbZGtkIhvNhRrpIBHBqz80'
LOCATION = '45.4215,-75.6972'  #user gotta input
RADIUS = 10000  # in meters (10 km)
park_and_ride_addresses = [
    "Woodroffe Ave. at Baseline Rd., across from Algonquin College, Ottawa, ON",
    "1580 Telesat Court, Ottawa, ON",
    "Canadian Tire Centre, Huntmar Dr. and Cyclone Taylor Blvd., Ottawa, ON",
    "2925 Navan Rd., NE corner of Brian Coburn Blvd. and Navan Rd., Ottawa, ON",
    "Highway 417 and Eagleson Rd., Ottawa, ON",
    "100 Via Park Place, Ottawa, ON",
    "Bank St. and Johnston Rd., Ottawa, ON",
    "Innovation Dr. and Terry Fox Dr., Ottawa, ON",
    "Bob MacQuarrie Recreation Complex, Youville Dr. and Jeanne d'Arc Blvd., Ottawa, ON",
    "Gilligan Rd., south of Leitrim Rd and west of Albion Rd., Ottawa, ON",
    "East of Trim Rd. on Millennium Blvd., Ottawa, ON",
    "Woodroffe Ave. and Strandherd Dr., Ottawa, ON",
    "Place d’Orléans Shopping Centre, Ottawa, ON",
    "Ray Friel Recreation Complex, Tenth Line Rd., Ottawa, ON",
    "Earl Armstrong Rd., Ottawa, ON",
    "3680 Strandherd Dr., Ottawa, ON",
    "Kanata Centrum Shopping Centre, off Highway 417, Ottawa, ON",
    "Trim Rd. and Highway 174, Ottawa, ON"
]
# Step 1: User inputs a location name
# origin = input("Enter a origin (e.g., uOttawa, Parliament Hill): ").strip()
# destination = input("Enter destination: ").strip()  # e.g., "Kanata, ON"
origin = "st benedict school ottawa"
destination = 'uottawa'
lowest1 = float('inf') # Smallest
lowest2 = float('inf') # Second smallest
lowest3 = float('inf') # Third smallest
address1 = ''
address2 = ''
address3 = ''
# User enters a date and time string (24-hour format)
# user_input = input("Enter departure date and time (YYYY-MM-DD HH:MM): ")  # e.g., 2025-08-06 08:30
user_input = "2025-08-05 08:27"
# Convert to datetime object
departure_datetime = datetime.datetime.strptime(user_input, "%Y-%m-%d %H:%M")

# Convert to Unix timestamp
departure_timestamp = int(time.mktime(departure_datetime.timetuple()))


# url = (
# "https://maps.googleapis.com/maps/api/directions/json"
# f"?origin={origin}"
# f"&destination={destination}"
# f"&mode=driving"
# f"&departure_time={departure_timestamp}"
# f"&traffic_model=best_guess"
# f"&key={API_KEY}"
# )

# # Make request
# response = requests.get(url).json()

# # Parse and display result
# if response['status'] != 'OK':
#     print("Error:", response.get('error_message', response['status']))
# else:
#     route = response['routes'][0]['legs'][0]

#     # duration of just car
#     drive_duration = route['duration_in_traffic']['value']
# print(sectomin(drive_duration))

# Step 2: Convert to coordinates using Geocoding API
geo_url = (
    'https://maps.googleapis.com/maps/api/geocode/json'
    f'?address={origin}&key={API_KEY}'
)

geo_response = requests.get(geo_url).json()
if not geo_response['results']:
    print("Location not found.")
    exit()

location = geo_response['results'][0]['geometry']['location']
latlng = f"{location['lat']},{location['lng']}"
print(f"Coordinates of '{origin}': {latlng}")

# Step 3: Search nearby places using Places API
results_seen = set()

for address in park_and_ride_addresses:
    
    # print(f"{query.upper()}: {name} - {address} ({lat}, {lng})")
    url = (
    "https://maps.googleapis.com/maps/api/directions/json"
    f"?origin={origin}"
    f"&destination={address}"
    f"&mode=driving"
    f"&departure_time={departure_timestamp}"
    f"&traffic_model=best_guess"
    f"&key={API_KEY}"
    )

    # Make request
    response = requests.get(url).json()

    # Parse and display result
    if response['status'] != 'OK':
        print("Error:", response.get('error_message', response['status']))
    else:
        route = response['routes'][0]['legs'][0]
        park_duration = route['duration_in_traffic']['value']
        if True:
            # print(f"Estimated driving time from {origin} to {address} at 8:30 AM Tuesday: {park_duration}")

            url = (
                "https://maps.googleapis.com/maps/api/directions/json"
                f"?origin={address}"
                f"&destination={destination}"
                f"&mode=transit"
                f"&departure_time={departure_timestamp}"
                f"&key={API_KEY}"
            )

            # Send request
            response = requests.get(url).json()

            # Parse and display results
            if response['status'] != 'OK':
                print("Error:", response.get('error_message', response['status']))
            else:
                leg = response['routes'][0]['legs'][0]
                ride_duration = leg['duration']['value']
                # if park_duration + ride_duration < shortest_duration:
                if True:
                    pnr_duration= park_duration + ride_duration
                    if pnr_duration< lowest1:
                        # Current duration is the new smallest
                        lowest3 = lowest2      # Old second duration becomes new third
                        address3 = address2    # Old second address becomes new third

                        lowest2 = lowest1      # Old first duration becomes new second
                        address2 = address1    # Old first address becomes new second

                        lowest1 = pnr_duration # Current is the new first duration
                        address1 = address  # Current is the new first address

                    elif pnr_duration< lowest2:
                        # Current duration is between the first and second lowest
                        lowest3 = lowest2      # Old second duration becomes new third
                        address3 = address2    # Old second address becomes new third

                        lowest2 = pnr_duration # Current is the new second duration
                        address2 = address  # Current is the new second address

                    elif pnr_duration< lowest3:
                        # Current duration is between the second and third lowest
                        lowest3 = pnr_duration # Current is the new third duration
                        address3 = address  # Current is the new third address                           
                    # print(f"leg arrival time {leg['duration']}")
                    # arrival = leg['arrival_time']['value']
                    
                    # departure = leg['departure_time']['value']
                    
                    print(f"park duration: {sectomin(park_duration)}")
                    print(f"ride duration: {sectomin(ride_duration)}")
                    # print(f"drive duration: {sectomin(drive_duration)}")
                    print(f"PnR location: {address}")
                    print(f"PnR: {sectomin(pnr_duration)}")

print(f"fastest: {sectomin(lowest1)} mins \n address: {address1}")

print(f"2nd fastest: {sectomin(lowest2)} mins \n address: {address2}")

print(f"3rd fastest: {sectomin(lowest3)} mins \n address: {address3}")
                    