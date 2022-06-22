import logging
logging.basicConfig(level=logging.DEBUG)

import urllib.request, json 

import os
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

import os
from slack import WebClient

# import config file with api keys
import config


# Free forecast API OpenMeteo
# Lat & Lon is set to Brno, CZ
forecastUrl = "https://api.open-meteo.com/v1/forecast?latitude=49.19&longitude=16.60&hourly=weathercode&timezone=Europe%2FBerlin"
# WMO Weather interpretation codes - these codes indicate possible rain
rainWeatherCodes = [61, 63, 65, 66, 67, 80, 81, 82]
# Forecast hours (this script will be called every morning in 7 am - so i do care only about next 15 hours to 10 pm)
forecastHours = 15  
client = WebClient(token=config.slack_api_key)

with urllib.request.urlopen(forecastUrl) as url:
    data = json.loads(url.read().decode())
    weatherForecast = data["hourly"]["weathercode"]
    if any(x in rainWeatherCodes for x in weatherForecast[:forecastHours]):
        # Send notification here
        print("It is gonna rain today!")
        try:
          response = client.chat_postMessage(
            channel=config.slack_channel_id,
            text="It is gonna rain today! Take an umbrella with you. :umbrella:"
          )
        except SlackApiError as e:
          assert e.response["error"] 

