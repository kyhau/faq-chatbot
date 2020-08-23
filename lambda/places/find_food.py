import logging
import os
from datetime import datetime

import googlemaps

logger = logging.getLogger()
logger.setLevel(logging.INFO)


google_api_key = os.environ["GoogleApiKey"]

gmaps = googlemaps.Client(key=google_api_key)


def lambda_handler(event, context):
    resp = gmaps.geocode("Flinders Street Station, Melbourne, Australia")
    logging.info(resp)
    latlong = resp[0]["geometry"]["location"]
    #latlong = {'lat': -37.8182711, 'lng': 144.9670618}
    logging.info(latlong)

    resp = gmaps.places(
        "restaurant",
        location=(latlong["lat"], latlong["lng"]),
        radius=5,
        region="AU",
        language="en-AU",
        min_price=1,
        max_price=50,
        open_now=True,
        type="food",
    )
    for item in resp["results"]:
        print(resp)


if __name__ == "__main__":
     lambda_handler(None, None)
