import os
import geocoder
from pyowm import OWM



class WeatherDetails:

    def __init__(self, unit, city, countrycode):
        self.unit= unit
        self.unitsymbol = self.getUnitSymbol()
        self.city=city
        self.countrycode=countrycode
        #owm weather manager related variables
        self.weatherdata=None
        self.__getWeatherData()
        

    # Convert a city name and country code to latitude and longitude
    def getCoords(self):
        # Get the latitude and longitude for our configured location
        location_string = "{city}, {countrycode}".format(city=self.city, countrycode=self.countrycode)
        g = geocoder.arcgis(location_string)
        coords = g.latlng
        return coords


    #Get the weather data for the given location using OpenWeatherMap API
    def __getWeatherData(self):
        #Get lat and long corresponding to the city/country
        coords = self.getCoords()

        #use OWM API to get the current weather information
        #OWM API key
        owmkey=os.getenv('OWM_KEY')
        if(owmkey==None):
            print('Error getting env data')
        else:
            try:
                owm = OWM(owmkey)
                owmMgr = owm.weather_manager()
                one_call = owmMgr.one_call(coords[0], coords[1])
                self.weatherdata=one_call
            except:
                print('Error getting weather information')

    
    #Get the symbol related to the temp unit
    def getUnitSymbol(self):
        symbol = None
        if(self.unit=='celsius'):
            symbol = ' °C'
        else:
            symbol = ' °F'
        return symbol
            
