from data_manager import DataManager
from flight_search import FlightSearch
from flight_data import FlightData

data = DataManager()

user_data = data.get_users_email()
user_email_list = []
for user in range(len(user_data)):
    user_email_list.append(user_data[user]['email'])

sheet_data = data.get_api()
IATA_list = []
for destination in range(len(sheet_data)):
    if sheet_data[destination]['iataCode'] == "":
        FlightSearch().update_IATA(sheet_data[destination])
        current_row = destination + 2
        data.put_api(current_row, sheet_data[destination])
    IATA_list.append(sheet_data[destination]['iataCode'])
for position in range(len(IATA_list)):
    from_position = IATA_list[0]
    IATA_list.remove(from_position)
    data_lowest_price = sheet_data[position]['lowestPrice']
    for IATA in IATA_list:
        first_attempt = FlightData().search_flight(from_position, to_iata=IATA, stopovers=0)
        FlightData().flight_without_stopovers(data_lowest_price, first_attempt, user_email_list)
        if first_attempt is None:
            second_attempt = FlightData().search_flight(from_position, to_iata=IATA, stopovers=1)
            FlightData().flight_with_stopovers(data_lowest_price, second_attempt, user_email_list)
            if second_attempt is None:
                continue
    IATA_list.append(from_position)
