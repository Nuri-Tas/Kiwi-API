import requests
import datetime
import json
import smtplib
import os

mail = os.environ["MAIL"]
password = os.environ["PASSWORD"]

kiwii_api = os.environ["KIWII_API"]
kiwii_endpoint = "https://tequila.kiwi.com/v2/search"


tomorrow = datetime.date.today() + datetime.timedelta(days=1)
date = tomorrow.strftime("%d/%m/%Y")


six_months_later_dt = datetime.datetime(2022,10,7)
six_months_later = six_months_later_dt.strftime("%d/%m/%Y")



header_kiwii = {
    "apikey": "FXJ43YJSJarxvHY-c9JnpJ0LZFdxm5GQ"
}


# get/query did not work. you may look at it later
# locations_response = requests.get("https://tequila-api.kiwi.com/locations/query", headers=header_kiwii)

#kiwii_response = requests.get("https://tequila-api.kiwi.com/v2/search?fly_from=LGA&fly_to=MIA&dateFrom=07/04/2022&dateTo=07/10/2022", headers=header_kiwii)

IATA_CODES = ["DPS", "MAD", "MEX", "PAR", "LON", "BER", "IFJ"]
lowest_price_per_city = []

for item in IATA_CODES:
    prices = []
    params_kiwii = {
        "fly_from": "IST",
        "fly_to": item,
        "date_from": date,
        "date_to": six_months_later,
        "curr": "TRY",
        "flight_type": "round",
        "return_from": datetime.date.today() + datetime.timedelta(days=7),
        "return_to": datetime.date.today() + datetime.timedelta(days=28),
        "max_stopovers": 0
    }

    kiwii_response = requests.get(f"https://tequila-api.kiwi.com/v2/search", params=params_kiwii, headers=header_kiwii)
    kiwi_flights = kiwii_response.json()

    with open("flights.json", "w") as flights_file:
        json.dump(kiwi_flights, flights_file, indent=4)

    with open("flights.json") as flights_file:
        flights_read = json.load(flights_file)
        for flight in flights_read["data"]:
            if item == flight["cityCodeTo"]:
              prices.append(flight["price"])
        lowest = min(prices, default=0)
        lowest_price_per_city.append(lowest)

print(lowest_price_per_city)


sheety_endpoint = "https://api.sheety.co/588351d63b78f74fceb6c2fc819d4371/cheapFlightTracker/sheet1"

sheety_response = requests.get("https://api.sheety.co/588351d63b78f74fceb6c2fc819d4371/cheapFlightTracker/sheet1")
sheety = sheety_response.json()

for i in range(len(lowest_price_per_city)):
    print(sheety["sheet1"][i]["price"])

#for i in range(len(lowest_price_per_city)):
#    if lowest_price_per_city[i] != 0:
#        if lowest_price_per_city[i] < sheety["sheet1"][i]["price"] :
#            connection = smtplib.SMTP("smtp.gmail.com")
#            connection.starttls()
#            connection.login(mail,password)
#            connection.sendmail(from_addr=mail,to_addrs="nuri.tass19@gmail.com",msg=f"Subject:Flight for {sheety['sheet1'][i]['price']}"
#                                                                                    f"\n\n flight found for {sheety['sheet1'][i]['city']} for {lowest_price_per_city[i]} euros")
#            connection.close()
#


sheety_params = {
        "sheet1": [
            {"city": "Bali",
             "IATA Code": "DPS",
             "Price": 300},
            {"city": "Madrid",
             "IATA Code": "MAD",
             "Price": 50},
            {"city": "Mexico",
             "IATA Code": "MEX",
             "Price": 43},
            {"city": "Paris",
             "IATA Code": "PAR",
             "Price": 40},
            {"city": "Berlin",
             "IATA Code": "BER",
             "Price": 50},
        ]
    }

