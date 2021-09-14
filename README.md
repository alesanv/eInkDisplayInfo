# eInkDisplayInfo: Raspberry Pi + eInk Display showing stock and weather information
Use an Inky pHAT eInk display with a Raspberry pi Zero W to show stock and weather information.

## About the Project:
I live in a place where some months have very different weather from day to day, so I am usually checking the weather mornings and evenings. Since I wanted to practice Python and had a Raspberry Pi, I decided to create a little application where the weather information was shown. While looking for displays I came across the eInk displays and decided that I wanted to use one of those. 

The *goal* of this project is to show Stock and Weather information using a Raspberry Pi Zero W with an eInk display.


### Material:
-	Raspberry Pi Zero W.
-	If your Raspberry Pi doesn’t have the 2x20 pin header, you’ll have to get one male header strip. There are two kinds of male header strips: 
    - the ones that require to be soldiered onto the Pi, 
    - and the ones that can be hammered onto the Pi. 
    - *Note:* I used the later kind, and it took me a while to hammer them down… still some pins kind of move, so my advice is to solder them or get a Pi with the header already attached.
-	Pimoroni Inky pHAT display.
-	MicroSD Card.


TODO: PICTURES!

---
## HARDWARE:

### Raspberry Pi Zero W:

The Raspberry Pi Zero W has built-in WiFi, it is very small and cheap. It has a micro SD card slot, a mini HDMI port, two micro USB ports (one for power, one for USB), 512 MB of RAM, a single-core 1GHz processor.

You’ll have to install the Raspberry Pi OS into the MicroSD card, the directions can be found in the official Raspberry Pi website on [how to set up your SD Card](https://projects.raspberrypi.org/en/projects/raspberry-pi-setting-up/2).


### Pimoroni Inky pHAT:

The Pimoroni Inky pHAT is a low-energy eInk display for the Raspberry Pi, it comes in three color schemes: red/black/white, yellow/black/white, and black/white. In this project I’m using a red/black/white display, it has a resolution of 212x104 pixels, there’s some later models with higher resolution (250x122 pixels). One of the features of eInk displays is that the image drawn on them persists even when no power is present. 


It is a beautiful display, fully-assembled, the same size of the Raspberry Pi Zero W, and you’ll just need to insert the Inky pHAT into your Raspberry Pi and run Pimoroni’s installer to get everything set up. Pimoroni offers a getting started guide, a Python library, and several examples ready to use with your Inky pHAT (like a name badge display example). The official tutorial to get started with Inky pHAT can be found at [getting started with inky phat](https://learn.pimoroni.com/article/getting-started-with-inky-phat).

TODO: 
PIC of how it looks!!

---
## SOFTWARE:

### Features:

The Inky pHAT is a small display, its size is approx. 1 in x 2.5 in, and it is not meant to be used with information that needs to be updated in real time. The information that I decided to show in the display is:
-	**IP Address:** To work with the Raspberry Pi more easily it is always convenient to know its IP address. 
-	**Current Weather:** I like checking the weather in a daily basis, so for me it is useful to show the current weather information and maybe in the future (when I get a bigger display) I could show forecast information. 
-	**Stock Prices:** stock information for three stocks will be shown.
-	**Time of last update:** it is always useful to know from which point in time is the information shown in the display. 


The idea is to run the Python script once every hour. Taking advantage of the fact that the Raspberry Pi OS is based on Debian we can add the script as a cron job that runs every hour.  

The application uses one configuration file where I store variables related to the Stock information and the Weather information.

The following picture shows a diagram of what I was trying to accomplish:

TODO: Photo of paper design


### Implementation:


**Stock details module:**

Since there’s a lot of interest in stocks, I decided to get stock information too. The scope of this app is not financial just informational, so the only thing of interest would be the stock price. I am using the Beautiful Soup library in Python to accomplish this; the library will allow me to get data from the Yahoo Finance website.  

There’s enough space to show three Stock prices, so they will be configurable. The configuration file will contain three entries, where the Stock's symbol has to be stored.


How it works:
1. The requests library is used to retrieve the HTML of whichever page you indicate. To get stock data the URL that I am using corresponds to the Yahoo Finance site. Example:
` https://finance.yahoo.com/quote/ETSY?p=ETSY&.tsrc=fin-srch`

2. Then we start our Beautiful Soup object indicating that it should parse the page through an XML parser.

3. After getting all the HTML ready to use I need to look for the stock price, which is inside it somewhere. To get a specific item from a webpage a tag and a class are needed. To get them we can use the Developer Tools in our browser and then select an element in the page to inspect it. 
TODO: PICTURE

4. After using Beautiful Soup to find that value in the HTML, the application has the stock price as shown in the site. 



**Weather module:**

I am using the Open Weather Map API (https://openweathermap.org/api).  To use the API you need to create an account because you will need the API key, there's a free tier. For this application the free subscription is enough. 

There is also a Python library called PyOWM which is a wrapper library for the Open Weather Map web API, so I am using it. 

My original plans had the display showing the forecast for tomorrow, but since the Inky pHAT is so small, it was not possible, but it is still something that I would like to do. With that in mind, I am using the Open Weather One Call API to get current weather and forecast data for any geographical coordinates. 


There are some variables that will be taken from a configuration file. Those are:
-	Temperature units: Celsius or Farenheit
-	City: City name
-	Country: Country code

 The Open Weather Map (OWM) API key will need to be exported to the OS environment in order to use it in the application.

 How it works:
 1. Convert a city name and country code to latitude and longitude with the geocoder Library.
 2. Using the pyowm library call the OWM One Call API to get the weather data. This way we will retrieve current and forecast information. I will show the Current temperature and Description in the eInk display.


**Network information module:**

To work with a Raspberry Pi it is always convenient to know its IP address, this is the reason behind obtaining this information. I am using the socket library to accomplish this. 

How it works:
1. I created a socket of the `AF_INET` family and type `SOCK_DGRAM`.
2. I try to connect to a dummy IP address, in this case I'm using a local network IP.
3. After that I will be able to retrieve the Raspberry Pi’s local IP address from the socket.  

**Display the information:**

The paths for the font and the background in use by the application have to be stored in the configuration file. 

How it works:
1. Prepare the Inky pHAT display by initializing it. 
2. Load the font that is going to be used.
3. Load the background image that will be shown.
4. Get all the information that will be displayed.
5. Draw the date, IP, Stocks and Weather information.
6. Update the eInk display.


### Installing the Application in the Raspberry Pi:

1. Clone this repository and store the files in your Raspberry Pi with the Inky pHAT eInk display. 

2. This project needs Python 3.7+ to run. Check your version running:
    ```bash
    python --version
    ```


3. First, as in any python project it is best to create its own virtual environment:
    ```python
    python -m venv env
    source env/bin/activate
    ```
    *Note: to deactivate the virtual environment just write `deactivate`*

4. Then we proceed to install all the project dependencies:

    ``` python
    pip install inky[rpi,fonts]
    pip install pillow
    pip install beautifulsoup4
    pip install lxml
    pip install requests
    pip install pyowm
    pip install geocoder
    ```

5. Update the `config.py` file with the information that you wish to show in the eInk display:
    | Name           | Description                  |
    |----------------|------------------------------|
    | FONT           | Path to the Font file        |
    | IMG_BACKGROUND | Path to the background image |
    | STOCK1         | Stock symbol #1              |
    | STOCK2         | stock symbol #2              |
    | STOCK3         | stock symbol #3              |
    | CITY           | city name                    |
    | COUNTRYCODE    | country code                 |
    | TEMP_UNIT      | Celsius or Farenheit         |

6. We need to export the OWM API key. We'll need to write the following line in the `~/.bashrc` file:
    ```bash
    export OWM_KEY='YOUR_KEY_HERE'
    ```

7. Test that your setup is working. Type the following in the command line:
    ``` bash
    python3 DisplayStockWeather.py
    ``` 
8. If your display can update without error we are ready to add our Script to the crontab. 
    - To do this the `DisplayStockWeather.py` script has to have executable permissions.
        ```bash
        sudo chmod +x DisplayStockWeather.py
        ```
    - You need to get the path for your Python environment.
        ```bash
        which python
        ```
    - You need to get the path to the script. 
        ```bash
        pwd
        ``` 
    - Now let's add the job to crontab:
        ```bash
        crontab -e
        ```
    - Add a line like the next one (updating according to your environment) to the crontab file to call the script every 10 minutes past the hour. If you want a different interval you can go to [crontab guru](https://crontab.guru/) to help you make the entry. **Log** information will be stored in the location indicated in the entry, including error information.

        ```
        *10 * * * * <PATH_TO_ENVIRONMENT> <PATH_TO_SCRIPT>/DisplayStockWeather.py >> <PATH_TO_WHERE_TO_STORE_LOGS>/<LOG_FILE_NAME> 2>&1
        ```

---

### Lessons learned:
When I started working on this project what made it not as easily to work on is that the Raspberry Pi had to be attached to a monitor, keyword and power source. So I was always stuck in a desk working on it, without the freedom or computational power that my laptop gives me. Because honestly the Raspberry Pi Zero W is not a fast computer. 

So I decided to work on each module on my laptop using Visual Studio while investigating how to get the data that I wanted to display. 

Then my hopes went up when I found out that [Visual Studio Code allows to code remotely on a Raspberry Pi](https://www.raspberrypi.org/blog/coding-on-raspberry-pi-remotely-with-visual-studio-code/), but that does not work for the Raspberry Pi Zero W... 

Then finally I found out that `Thonny` allows to connect to the Raspberry Pi Zero W over SSH and that I could connect the Pi to my laptop to serve as power source. 

So I would recommend to use Visual Studio to develop your code that does not depend on the display, that way you can easily debug and test that it works. Once that code is ready you can use Thonny to work on everything related to the Inky pHAT connecting your Pi to your computer. 

Another problem was working on the background image. Pimoroni has all the information needed to create images compatible with the display, but they involve `Gimp` and it is really slow in the Raspberry Pi Zero W. That is why the background is very basic so far. Hopefully I can improve it in the future. 


