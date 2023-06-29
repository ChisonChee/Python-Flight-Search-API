import requests
PRICE_ENDPOINTS = "https://api.sheety.co/YOUR_SHEETY_API_KEY/flightDeals/prices"
USER_ENDPOINTS = "https://api.sheety.co/YOUR_SHEETY_API_KEY/flightDeals/users"


class DataManager:
    def __init__(self):
        self.request = None
        self.update = None
        self.data = None

    def get_api(self):
        self.data = requests.get(url=PRICE_ENDPOINTS)
        self.data.raise_for_status()
        return self.data.json()['prices']

    def put_api(self, row, iata):
        params = {
            'price': {
                'iataCode': iata['iataCode']
            }
        }
        self.update = requests.put(url=f"{PRICE_ENDPOINTS}/{row}", json=params)

    def get_users_email(self):
        self.request = requests.get(url=USER_ENDPOINTS)
        self.request.raise_for_status()
        return self.request.json()['users']
