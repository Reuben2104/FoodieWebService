from flask import Flask, request
import json
import requests

app = Flask(__name__)

class GeocodioClient(object):
    def __init__(self, api_key):
        self.base_url = 'https://api.geocod.io/v1.6'
        self.api_key = api_key

    def request(self, addr):
        url = f'{self.base_url}/geocode?q={addr}&api_key={self.api_key}'
        response = requests.get(url)
        if response.status_code == 200:
            data = json.loads(response.text)
            location = data['results'][0]['location']
            return (location['lat'], location['lng'])
        else:
            print(f'Error geocoding address "{addr}": {response.status_code} {response.text}')

class YelpClient(object):
    def __init__(self, api_key):
        self.base_url = 'https://api.yelp.com/v3'
        self.api_key = api_key

    def request(self, latitude, longitude):
        url = f'{self.base_url}/businesses/search'
        headers = {'Authorization': f'Bearer {self.api_key}'}
        params = {'latitude': latitude, 'longitude': longitude, 'categories': 'restaurants'}
        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:
            data = json.loads(response.text)
            return [{'name': b['name'], 'rating': b['rating'], 'address': ', '.join(b['location']['display_address'])} for b in data['businesses']]
        else:
            print(f'Error searching for restaurants: {response.status_code} {response.text}')

# Initialize client objects with API keys
geocodio_client = GeocodioClient('2f62af5df46328e812a0a142ffd0e4f42d81e06')
yelp_client = YelpClient('aynfleJ2zfDte3lEZ41zG6V55AL7vrJxnjvtDhCXAkOsUVWVJTzXmbFHxiHHPWxssTwzipoEa5hgLvY8YrK6OOv9i2omUCKvde5qBfJTNAFw3wheRivHQXNJst8YZHYx')

@app.route('/restaurant/<restaurant_addr>', methods=['GET'])
def restaurant(restaurant_addr):
    if request.method == 'GET':
        # Get latitude and longitude from Geocodio API
        lat, lng = geocodio_client.request(restaurant_addr)
        if lat is not None and lng is not None:
            # Get nearby restaurants from Yelp API
            restaurants = yelp_client.request(lat, lng)
            if restaurants is not None:
                restaurants_dict = {"restaurants": restaurants}
                print(json.dumps(restaurants_dict, indent = 4))
                return json.dumps(restaurants_dict, indent = 4)
            else:
                return 'Error retrieving restaurants from Yelp API.'
        else:
            return 'Error retrieving latitude and longitude from Geocodio API.'
    else:
        return 'Invalid request.'

if __name__ == '__main__':
    app.run()


