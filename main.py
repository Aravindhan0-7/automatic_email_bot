import requests
from datetime import datetime
import smtplib
import time

MY_EMAIL = 'EMAIL_ID'
MY_PASSWORD = 'PASSWORD'
MY_LAT = LATITUDE # Your latitude
MY_LONG = LONGITUDE # Your longitude

def iss_overhead():
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    data = response.json()

    iss_latitude = float(data["iss_position"]["latitude"])
    iss_longitude = float(data["iss_position"]["longitude"])

    if MY_LAT-5<= iss_latitude <=MY_LAT+5 and MY_LONG-5<= iss_longitude <=MY_LONG+5:
        return True


def is_night():
    parameters = {
        "lat": MY_LAT,
        "lng": MY_LONG,
        "formatted": 0,
    }

    response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()
    data = response.json()
    sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])

    time_now = datetime.now()
    if time_now.hour >= sunset and time_now.hour <= sunrise:
        return True
while True:
    time.sleep(60)
    if is_night() and iss_overhead():
        connection= smtplib.SMTP("smtp.gmail.com")
        connection.login(MY_EMAIL,MY_PASSWORD)
        connection.starttls()
        connection.sendmail(from_addr=MY_EMAIL,to_addrs="SENDER_EMAIL_ID",msg="subject=iss_tracker\n\n the iss is above you look up!")
        connection.close()



# BONUS: run the code every 60 seconds.



