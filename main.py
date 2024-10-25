import os
import time
import requests
from dotenv import load_dotenv
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

load_dotenv()

API_KEY = os.getenv('11aa52840c851a872b2d4f2a9b56c456')
SENDER_EMAIL = os.getenv('jalajayaprakash8@gmail.com')
SENDER_PASSWORD = os.getenv('jayaprakash8')
RECEIVER_EMAIL = os.getenv('jayaprkash_jala@srmap.edu.in')

CITIES = ["Delhi", "Mumbai", "Chennai", "Bangalore", "Kolkata", "Hyderabad"]
INTERVAL = 300

ALERT_THRESHOLD_TEMP = 35
ALERT_CONSECUTIVE_COUNT = 2

consecutive_high_temp_count = {city: 0 for city in CITIES}

def get_weather_data(city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    return None

def convert_kelvin_to_celsius(temp_kelvin):
    return temp_kelvin - 273.15

def process_weather_data(data):
    temp_celsius = convert_kelvin_to_celsius(data['main']['temp'])
    feels_like_celsius = convert_kelvin_to_celsius(data['main']['feels_like'])
    main_condition = data['weather'][0]['main']
    timestamp = data['dt']
    return temp_celsius, feels_like_celsius, main_condition, timestamp

def send_alert_email(subject, body):
    if not (SENDER_EMAIL and SENDER_PASSWORD and RECEIVER_EMAIL):
        print("Email settings are not configured properly.")
        return

    message = MIMEMultipart()
    message["From"] = SENDER_EMAIL
    message["To"] = RECEIVER_EMAIL
    message["Subject"] = subject

    message.attach(MIMEText(body, "plain"))

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, message.as_string())
        server.quit()
        print("Alert email sent successfully.")
    except Exception as e:
        print(f"Failed to send email: {e}")

def check_alert_conditions(city, temp):
    global consecutive_high_temp_count
    if temp > ALERT_THRESHOLD_TEMP:
        consecutive_high_temp_count[city] += 1
    else:
        consecutive_high_temp_count[city] = 0

    if consecutive_high_temp_count[city] >= ALERT_CONSECUTIVE_COUNT:
        subject = f"Weather Alert for {city}"
        body = f"The temperature in {city} has exceeded {ALERT_THRESHOLD_TEMP}°C for {ALERT_CONSECUTIVE_COUNT} consecutive readings."
        print(f"Triggered alert for {city}: {body}")
        send_alert_email(subject, body)
        consecutive_high_temp_count[city] = 0

def main():
    while True:
        for city in CITIES:
            weather_data = get_weather_data(city)
            if weather_data:
                temp, feels_like, condition, timestamp = process_weather_data(weather_data)
                print(f"City: {city}, Temp: {temp}°C, Feels Like: {feels_like}°C, Condition: {condition}")
                check_alert_conditions(city, temp)
        time.sleep(INTERVAL)

if __name__ == "__main__":
    main()
