import requests
import json
from datetime import datetime

now = datetime.now()
date = now.strftime("%d/%m/%Y")

six_months_later_dt = datetime(2022,10,7)
six_months_later = six_months_later_dt.strftime("%d/%m/%Y")

prices = []
params_kiwii = {
    "fly_from": "IST",
    "fly_to": "DPS",
    "date_from": date,
    "date_to": six_months_later,
}

header_kiwii = {
    "apikey": "FXJ43YJSJarxvHY-c9JnpJ0LZFdxm5GQ"
}

kiwii_response = requests.get(f"https://tequila-api.kiwi.com/v2/search", params=params_kiwii, headers=header_kiwii)
kiwi_flights = kiwii_response.json()
print(kiwi_flights)