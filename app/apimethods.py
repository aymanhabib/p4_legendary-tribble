import requests, json
import os

import swagger_client
from swagger_client.rest import ApiException
# str | Account api key, to be used in every api call
swagger_client.configuration.api_key['apikey'] = "210c21424f9895ccb3c6274d003b09d9"

# create an instance of the API class
api_instance = swagger_client.AlbumApi()

track_id=15953433

print(api_instance.trackGetGet(track_id))
