# Import libraries
import json
import os
import string

import discord
import requests
from dotenv import load_dotenv

# Base url for api call
base_url = "http://api.weatherapi.com/v1"
# API Key from weather api site
API_KEY = "c07276ba07d641d89fb170830230104"
# This is the link attached to baase  url
forecast = "/forecast.json"

# To get name of all cities
url_forecast = "https://raw.githubusercontent.com/lutangar/cities.json/master/cities.json"
# request to fetch information
location=[]
response_f = requests.request("GET", url_forecast )
data = json.loads(response_f.text)

# print(data)
for i in data:
    loc = i['name']
    location.append(loc)



# Function to get the information about city
def get_info(city):
    # Complete url
    url_forecast = f"{base_url}{forecast}?key={API_KEY}&q={city}"
    # request to fetch information
    response_f = requests.request("GET", url_forecast )
    # To check if status code is 200
    status = response_f.status_code
    if status == 200:
        response_f = json.loads(response_f.text)
        return response_f,status
    # If status code is not 200
    else :
        return response_f,status
# Python-dotenv reads key-value pairs from a .env file and can set them as environment variables
load_dotenv()
# TOKEN and GUILD are variables from .env file
TOKEN = os.getenv("DISCORD_TOKEN")
GUILD = os.getenv("DISCORD_GUILD")
# The intents that are necessary for your bot can only be dictated by yourself
intents = discord.Intents.default()
intents.members = True
intents.message_content = True
# Represents a client connection that connects to Discord. This class is used to interact with the Discord WebSocket and API.
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f"We have logged in as {client.user}")

@client.event
async def on_message(message):
    # If the message is from bot just ignore that message and do nothing
    if message.author == client.user:
        return
    # If message is help then it will show a message
    if message.content == 'Hi':
        await message.channel.send("Hello this is a Weather API Bot.")
    elif message.content[0:11]== 'How are you':
        await message.channel.send("I am fine! Thank You!")
    elif message.content == '!w-help':
        # await message.channel.send is used to send message to channel
        await message.channel.send("!help command :")
        await message.channel.send("!w-<City> -- This will give some weather information about eneterd valid city")
    # if meesage starts with !w- or w. and ends with a city name it will give the details of that city weather
    elif message.content[0:3] == '!w-':
        if message.content[3:] in location:
            city = message.content[3:]
            # we are calling a function here
            info,status = get_info(city)
            # if function returns 200 as status then
            if status == 200:
                await message.channel.send(f"Here is the weather data for {city.title()} city")
                await message.channel.send("Temperature in Celcius")
                # info will have all the details about that city weather
                await message.channel.send(info['current']['temp_c'])
                await message.channel.send("Feels like")
                await message.channel.send(info['current']['feelslike_c'])
                await message.channel.send("Minimum Temperature")
                await message.channel.send(info['forecast']['forecastday'][0]['day']['mintemp_c'])
                await message.channel.send("Maximum Temperature")
                await message.channel.send(info['forecast']['forecastday'][0]['day']['maxtemp_c'])
            # if any other message is displayed it will throw an error
    else :
        await message.channel.send("Error ! Please enter valid city name or you can enter !w-help to get some help")
    
# Providing token stored in .env file
client.run(TOKEN)