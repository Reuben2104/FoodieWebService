import requests
import json

class FoodieClient(object):
    """
    The client that sends requests to the Foodie Web Service.
    """
    def __init__(self, base_url):
        self.base_url = base_url

    def search_restaurants(self, address):
        url = f'{self.base_url}/restaurant/{address}'
        response = requests.get(url)
        if response.status_code == 200:
            restaurants = json.loads(response.text)
            print(f'Restaurants near {address}:')
            for restaurant in restaurants:
                print(f"{restaurant['name']} ({restaurant['rating']}) - {restaurant['address']}")
        else:
            print(f'Error searching for restaurants: {response.status_code} {response.text}')
