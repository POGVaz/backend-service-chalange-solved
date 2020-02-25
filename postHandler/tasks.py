from .models import Address
from celery import shared_task
import googlemaps

# This might not work without a proper key.
google_client = googlemaps.Client(key='')

@shared_task
def fetch_location(address_id, street, city, state):
    # Fetch location from Google Maps API
    geocode_result = google_client.geocode('{}, {}, {}'.format(street, city, state))
    result_latitude = geocode_result[0]["geometry"]["location"]["lat"]
    result_longitude = geocode_result[0]["geometry"]["location"]["lng"]

    # Update the address with the location
    address_to_update = Address.get(pk=address_id)
    address_to_update.set(latitude=result_latitude, longitude=result_longitude)
