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
font = ImageFont.truetype("Resources/Roboto-Light.ttf",12)


#Load background
print("Loading background...")
img = Image.open("Resources/bg1.png")
draw = ImageDraw.Draw(img)


    
#w, h = font.getsize(message)
#x = (inky_display.WIDTH / 2) - (w / 2)
#y = (inky_display.HEIGHT / 2) - (h / 2)
#draw.text((x, y), message, inky_display.RED, font)


#Get Local IP Address
deviceNet = DeviceNetworkDetails()
print("IP Address: " + deviceNet.ip_addr)

#Get the Current weather information
cityWeather = WeatherDetails(config.TEMP_UNIT, config.CITY, config.COUNTRYCODE)
current_temp = cityWeather.weatherdata.current.temperature(cityWeather.unit).get('temp', None)
print("Current Temp: " + str(current_temp) + cityWeather.unitsymbol)
current_weather_status = cityWeather.weatherdata.current.status
print("Main description: " + str(current_weather_status) )



#Grab GME stock price
gme = Stock('Game Stop','GME')
print(gme)

#Grab Etsy stock price
etsy = Stock('Etsy','ETSY')
print(etsy)

#Grab Target stock price
target = Stock('Target','TGT')
print(target)

# Grab the current date
now = datetime.datetime.now()
print("Date: " + now.strftime("%d/%m/%y"))


# Get text ready to print on the e-ink screen
#Draw DATE
draw.text((6,84), "Last update: " + now.strftime("%m/%d/%y @ %H:%M"), inky_display.BLACK, font)

#Draw Local IP ADDRESS
draw.text((6, 4), "IP: " + deviceNet.ip_addr, inky_display.BLACK, font)

#Draw stock1 price
draw.text((6, 20), str(etsy), inky_display.RED, font)

#Draw stock2 price
draw.text((6,40), str(gme), inky_display.RED, font)

#Draw stock3 price
draw.text((6,60), str(target), inky_display.RED, font)

#Display weather
draw.text((110,30), "Temp: " + str(current_temp) + cityWeather.unitsymbol, inky_display.WHITE, font)
draw.text((110,50), str(current_weather_status), inky_display.WHITE, font)

#Display the Data
inky_display.set_image(img)
inky_display.show()


