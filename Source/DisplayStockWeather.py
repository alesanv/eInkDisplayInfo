#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import datetime
import config
from DeviceNetworkDetails import DeviceNetworkDetails
from StockData import Stock
from Forecast import WeatherDetails
from inky import InkyPHAT
from PIL import Image, ImageFont, ImageDraw



    
#=============================
#Display Data in an inkyphat e-Ink display
#Information to display:
#    - RaspberryPi's IP address
#    - Stock prices
#    - Current weather for location configured in file
#    - Date and time of last update
#=============================

#Prepare our inkyphat display
inky_display = InkyPHAT("red")
inky_display.set_border(inky_display.WHITE)
img = Image.new("P", (inky_display.WIDTH, inky_display.HEIGHT))

#Load Fonts
print("Loading fonts...")
font = ImageFont.truetype(config.FONT,12)


#Load background
print("Loading background...")
img = Image.open(config.IMG_BACKGROUND)
draw = ImageDraw.Draw(img)


# -- Get Local IP Address
deviceNet = DeviceNetworkDetails()
print(f"IP Address: {deviceNet.ip_addr}")

# -- Get the Current weather information
cityWeather = WeatherDetails(config.TEMP_UNIT, config.CITY, config.COUNTRYCODE)

if(cityWeather.weatherdata != None):
    #OWM information was retrieved successfully
    current_temp = cityWeather.weatherdata.current.temperature(cityWeather.unit).get('temp', None)
    print(f"Current Temp: {current_temp} {cityWeather.unitsymbol}")
    current_weather_status = cityWeather.weatherdata.current.status
    print(f"Main description: {current_weather_status}" )
else:
    #There was an error getting the OWM information
    current_temp = "ERR"
    current_weather_status = "ERROR"


# -- Grab stock Prices
#Grab first stock price
stock1 = Stock(config.STOCK1)
print(stock1)

#Grab second stock price
stock2 = Stock(config.STOCK2)
print(stock2)

#Grab third stock price
stock3 = Stock(config.STOCK3)
print(stock3)

# -- Grab the current date
now = datetime.datetime.now()
print(f'Date: {now.strftime("%m/%d/%y @ %H:%M")}')


# -- Get text ready to print on the e-ink screen
#Draw DATE
draw.text((6,84), f'Last update: {now.strftime("%m/%d/%y @ %H:%M")}', inky_display.BLACK, font)

#Draw Local IP ADDRESS
draw.text((6, 4), f"IP: {deviceNet.ip_addr}", inky_display.BLACK, font)

#Draw stock1 price
draw.text((6, 20), str(stock1), inky_display.RED, font)

#Draw stock2 price
draw.text((6,40), str(stock2), inky_display.RED, font)

#Draw stock3 price
draw.text((6,60), str(stock3), inky_display.RED, font)

#Display weather
draw.text((110,30), f"Temp: {current_temp} {cityWeather.unitsymbol}", inky_display.WHITE, font)
draw.text((110,50), str(current_weather_status), inky_display.WHITE, font)

#Display the Data
inky_display.set_image(img)
inky_display.show()


