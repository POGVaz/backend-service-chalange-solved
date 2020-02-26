from .models import Address
from celery import shared_task
import googlemaps

# This won't work without a proper key.
# google_client = googlemaps.Client()

#Fake client for google API, since we don't have a key:
class FakeClient:
    def geocode(self):
        print("Fake API call")
google_client = FakeClient()

@shared_task
def fetch_location(address_id, street, city, state):
    # Fetch location from Google Maps API
    geocode_result = google_client.geocode('{}, {}, {}'.format(street, city, state))
    result_latitude = geocode_result[0]["geometry"]["location"]["lat"]
    result_longitude = geocode_result[0]["geometry"]["location"]["lng"]

    # Update the address with the location
    address_to_update = Address.objects.get(pk=address_id)
    address_to_update.latitude = result_latitude
    address_to_update.longitude = result_longitude
    address_to_update.save()

# geocode result exemple:
# [
#   {'address_components': [
#       {
#          'long_name': 'Canada',
#          'short_name': 'CA',
#          'types': ['country', 'political']
#       }
#   ],
#   'formatted_address': 'Canada',
#   'geometry': {
#       'bounds': {
#           'northeast': {
#               'lat': 83.6381,
#               'lng': -50.9766},
#           'southwest': {
#               'lat': 41.6765559,
#               'lng': -141.00187
#           }
#       },
#       'location': {
#           'lat': 56.130366,       <-Info that we
#           'lng': -106.346771      <- are looking for
#        },
#       'location_type': 'APPROXIMATE',
#       'viewport': {
#           'northeast': {
#               'lat': 70,
#               'lng': -50
#           },
#           'southwest': {
#               'lat': 42,
#               'lng': -142
#           }
#       }
#   },
#   partial_match': True,
#   'place_id': 'ChIJ2WrMN9MDDUsRpY9Doiq3aJk',
#   'types': ['country', 'political']}
# ]
