import requests
import datetime as dt
from notification_manager import NotificationManager

tmr_date = dt.datetime.today() + dt.timedelta(days=1)
date_aft_6months = tmr_date + dt.timedelta(days=6 * 30)
tmr_date = tmr_date.strftime("%d/%m/%Y")
date_aft_6months = date_aft_6months.strftime("%d/%m/%Y")

ENDPOINTS = "https://api.tequila.kiwi.com/v2/search"
HEADER = {
    "apikey": "YOUR_API_KEY"
}


class FlightData:
    def __init__(self):
        self.via_city = ""

    def search_flight(self, from_iata, to_iata, stopovers):
        params = {
            "fly_from": f"{from_iata}",
            "fly_to": f"{to_iata}",
            "date_from": f"{tmr_date}",
            "date_to": f"{date_aft_6months}",
            "nights_in_dst_from": 7,
            "nights_in_dst_to": 28,
            "flight_type": "round",
            "one_for_city": 0,
            "max_stopovers": stopovers,
            "curr": "MYR"
        }
        request = requests.get(url=ENDPOINTS, headers=HEADER, params=params)
        request.raise_for_status()
        request = request.json()
        return request

    def flight_without_stopovers(self, data_lowest_price, returned_data, user_list):
        request = returned_data
        try:
            flight_data = {
                "cheapest_price": request['data'][0]['price'],
                "from_iata": request['data'][0]['cityCodeFrom'],
                "to_iata": request['data'][0]['cityCodeTo'],
                "from_city": request['data'][0]['cityFrom'],
                "to_city": request['data'][0]['cityTo'],
                "from_date": request['data'][0]['route'][0]['utc_departure'].split("T")[0],
                "to_date": request['data'][0]['route'][1]['utc_arrival'].split("T")[0]
            }
        except IndexError:
            return None
        else:
            NotificationManager(data_lowest_price, flight_data, self.via_city, user_list)

    def flight_with_stopovers(self, data_lowest_price, returned_data, user_list):
        request = returned_data
        try:
            if len(request['data'][0]['route']) == 3:
                self.via_city = request['data'][0]['route'][0]['fly_to']
            elif len(request['data'][0]['route']) == 4:
                if request['data'][0]['route'][0]['fly_to'] == request['data'][0]['route'][2]['fly_to']:
                    self.via_city = [request['data'][0]['route'][0]['fly_to']]
                else:
                    self.via_city = [request['data'][0]['route'][0]['fly_to'], request['data'][2]['route'][2]['fly_to']]
            flight_data = {
                "cheapest_price": request['data'][0]['price'],
                "from_iata": request['data'][0]['cityCodeFrom'],
                "to_iata": request['data'][0]['cityCodeTo'],
                "from_city": request['data'][0]['cityFrom'],
                "to_city": request['data'][0]['cityTo'],
                "from_date": request['data'][0]['route'][0]['utc_departure'].split("T")[0],
                "to_date": request['data'][0]['route'][2]['utc_arrival'].split("T")[0]
            }
        except IndexError:
            return None
        else:
            NotificationManager(data_lowest_price, flight_data, self.via_city, user_list)
