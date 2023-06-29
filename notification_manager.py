import smtplib


class NotificationManager:
    def __init__(self, flight_data, search_data, stopover, user_email):
        self.data_price = flight_data
        self.searched_price = search_data['cheapest_price']
        self.to_iata = search_data['to_iata']
        self.from_iata = search_data['from_iata']
        self.to_city = search_data['to_city']
        self.from_city = search_data['from_city']
        self.from_date = search_data['from_date']
        self.to_date = search_data['to_date']
        self.stopovers = stopover
        self.user_email = user_email
        if self.searched_price < self.data_price:
            self.notification()

    def notification(self):
        FLIGHT_URL = f"https://www.google.com/travel/flights?q=Flights%20to%20{self.to_iata}%20from%20{self.from_iata}%20on%20{self.from_date}%20through%20{self.to_date}"
        if len(self.stopovers) == 0:
            message = f"Subject: LOW PRICE ALERT!\n\n Only RM{self.searched_price} from {self.from_city}-{self.from_iata} " \
                      f"to {self.to_city}-{self.to_iata}, from {self.from_date} to {self.to_date}.\n\n{FLIGHT_URL}"
        elif len(self.stopovers) == 1:
            message = f"Subject: LOW PRICE ALERT!\n\n Only RM{self.searched_price} from {self.from_city}-{self.from_iata} " \
                      f"to {self.to_city}-{self.to_iata}, from {self.from_date} to {self.to_date}.\n\nFlight has 1 " \
                      f"stopover, via {self.stopovers}\n\n{FLIGHT_URL}"
        elif len(self.stopovers) > 1:
            message = f"Subject: LOW PRICE ALERT!\n\n Only RM{self.searched_price} from {self.from_city}-{self.from_iata} " \
                      f"to {self.to_city}-{self.to_iata}, from {self.from_date} to {self.to_date}.\n\nFlight has 2 " \
                      f"stopover, via {self.stopovers[0]} and {self.stopovers[1]}\n\n{FLIGHT_URL}"
        MY_EMAIL = "YOUR_EMAIL"
        PW = "YOUR_EMAIL_PASSWORD"
        for user in self.user_email:
            with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
                connection.starttls()
                connection.login(user=MY_EMAIL, password=PW)
                connection.sendmail(
                    from_addr=MY_EMAIL,
                    to_addrs=user,
                    msg=message.encode("utf-8")
                )