import argparse
from pysimplesoap.client import SoapClient
from concurrent.futures import ThreadPoolExecutor
import time

def query_server(location, user_city):
    server = SoapClient(
            location=location,
            namespace="http://xmlsoap.org/geolocation",
            trace=False,
        )
    response = server.getCity(city=user_city)
    return response


parser = argparse.ArgumentParser(description="SOAP Client")
parser.add_argument("--user_city", default="city", help="City name of the user")
parser.add_argument("--url", action="append", help="SOAP server url")
    
args = parser.parse_args()
if args.url is None:
    args.url = ['http://localhost:8000/']
    
while True:
    with ThreadPoolExecutor(max_workers=1) as executor:
        futures = [executor.submit(query_server, client, args.user_city) for client in args.url]

        for i, future in enumerate(futures, start=1):
            response = future.result()
            if response is not None and 'city' in response:
                city = response.city
                if city == "Not found":
                    print(f"Car {i} not in the same city as User.")
                else:
                    latitude = response.latitude
                    longitude = response.longitude
                    print(f"{i}: {city=} {latitude=} {longitude=}")
            else:
                print(f"Error: No response received from car {i}")
        time.sleep(2)
