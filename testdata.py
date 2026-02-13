import requests
from datetime import datetime
import csv

platitude_url= "http://192.168.3.141:8000/"
plate = "ABC123"

plate1 = {"code": "XYZ789"}
plate2 = {"code": "ABC123"}
#time = datetime.now()
###POST TEST PLATES
requests.post(f"{platitude_url}plates/", json=plate1)
requests.post(f"{platitude_url}plates/", json=plate2)
#GET TEST PLATES FOR TEST SIGHTINGS 
plate1data = requests.get(f"{platitude_url}plates/code/XYZ789").json()
plate2data = requests.get(f"{platitude_url}plates/code/ABC123").json()
print(plate1data)
plate1_id = plate1data["id"]
plate1_sighting1 = {
           "longitude": -122.4194,
           "latitude": 37.7749,
           "timestamp": "2026-02-12T14:30:00Z",

           "plate_id": plate1_id
         }

plate1_sighting2 = {
           "longitude": -133.4194,
           "latitude": 38.7749,
           "timestamp": "2026-02-10T06:30:00Z",

           "plate_id": plate1_id
         }

plate2_id = plate2data["id"]
plate2_sighting1 = {
           "longitude": -133.4194,
           "latitude": 38.7749,
           "timestamp": "2026-02-10T06:30:00Z",

           "plate_id": plate2_id
         }

plate2_vehice = {
           "make": "Ford",
           "model": "Focus",
           "year": "2019",
           "color": "red"
         }
#vehicle = requests.post(f"{platitude_url}/vehicles/", json=plate2_vehice)
#vehicle_json = vehicle.json()
#print(type(vehicle_json))
#plate2_vehicle_id = vehicle_json['id']
#print(plate2_vehicle_id)


'''
plate2_vehice_json = {
           "vehicle_id": {plate2_vehicle_id},

         }
'''

#requests.put(f"{platitude_url}/plates/{plate2_id}", json=plate2_vehice_json)
requests.post(f"{platitude_url}/sightings/", json=plate1_sighting1)
requests.post(f"{platitude_url}/sightings/", json=plate1_sighting2)
requests.post(f"{platitude_url}/sightings/", json=plate2_sighting1)
#print(response)
#plates = requests.get(url=f"{platitude_url}/plates/code/XYZ789")
#sightings = requests.get(url=f"{platitude_url}/sightings/")
#sighting_data = sightings.json()
#print(sighting_data)
#print(plates)
#data = plates.json()
#print(data)