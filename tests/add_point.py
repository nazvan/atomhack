import requests
from time import time, sleep
import json
import random

ip_address = '176.99.135.63'

(lat_1, lon_1), (lat_2, lon_2) = (55.7389, 37.6831),(55.7681, 37.5224)
response = requests.get(f'https://routing.openstreetmap.de/routed-car/route/v1/driving/{lon_1},{lat_1};{lon_2},{lat_2}?geometries=polyline&steps=true')
routes = json.loads(response.content.decode('utf-8'))['routes'][0]['legs'][0]['steps']
for point in routes:
    lat, lon = point['maneuver']['location']
    point_data = {
        'robotId':'3',
        'latitude':lon,
        'longitude':lat,
        'timestamp': int(time()),
        }
    point = requests.post(f'http://{ip_address}:8000/api/add_point', json=point_data)
    if random.randint(0,100)>50:
        defect_data = {
        'robotId':'1',
        'latitude':lon,
        'longitude':lat,
        'timestamp': int(time()),
        'imageId':'null',
        'type':'u'
        }
        print(defect_data)
        defect = requests.post(f'http://{ip_address}:8000/api/add_defect', json=defect_data)
    sleep(3)