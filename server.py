from pysimplesoap.server import SoapDispatcher, SOAPHandler
from http.server import HTTPServer
import random
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--city', type=str, help='City name',default="city")
parser.add_argument('--latitude', type=float, help='City latitude', default=0.0)
parser.add_argument('--longitude', type=float, help='City longitude', default=0.0)
parser.add_argument('--port', type=int, help='Port number', default=8000)
parser.add_argument('--hostname', type=str, help='hotname', default="localhost")

args = parser.parse_args()

dispatcher = SoapDispatcher(
    'geolocation',
    location=(args.hostname, args.port),
    namespace="http://xmlsoap.org/geolocation",
    trace=False,
)

if args.city and args.latitude is not None and args.longitude is not None:
    city_data = {
        "city": args.city,
        "latitude": args.latitude,
        "longitude": args.longitude
    }

def getCity(city):
    if city in city_data["city"]:
        latitude = city_data["latitude"] + random.uniform(0, 0.001) * random.choice([1, -1])
        longitude = city_data["longitude"] + random.uniform(0, 0.001) * random.choice([1, -1])
        return {"city": city, "latitude": latitude, "longitude": longitude}
    else:
        return {"city": "Not found", "latitude": 0.0, "longitude": 0.0}

dispatcher.register_function('getCity', getCity, returns={'city': str, 'latitude': float, 'longitude': float}, args={'city': str})
server = HTTPServer((args.hostname, args.port), SOAPHandler)
server.dispatcher = dispatcher
print(f"Geo-locator of the car started on http://{args.hostname}:{args.port}")
server.serve_forever()
