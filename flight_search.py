import requests

TEQUILA_IATA_ENPOINTS = "https://api.tequila.kiwi.com/locations/query"
TEQUILA_API_KEY = "YOUR_API_KEY"

HEADERS = {
    "apikey": TEQUILA_API_KEY
}


class FlightSearch:
    def update_IATA(self, iata):
        params = {
            "term": iata['city'],
            "location_types": "airport",
        }
        iata_get = requests.get(url=TEQUILA_IATA_ENPOINTS, headers=HEADERS, params=params)
        iata_get.raise_for_status()
        iataCode = iata_get.json()['locations'][0]['city']['code']
        iata['iataCode'] = iataCode
