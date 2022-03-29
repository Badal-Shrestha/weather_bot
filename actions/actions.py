# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import requests

PARAM = {'access_key': '', 'query': '', 'units': 'f'}
URL = "http://api.weatherstack.com/current"
PARAM['access_key'] = 'fb6c53c837ca70cd933868e7f5a869ed'
def get_weather(city):
    PARAM['query'] = city
    
    r = requests.get(url=URL,params=PARAM)
        
    return r.json()
class ActionGetWeather(Action):


    def name(self) -> Text:
        return "action_get_weather"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        ent = tracker.latest_message['entities'][0]['value']
        # import pdb; pdb.set_trace()
        data = get_weather(ent)
        city = data['location']['name']
        condition = data['current']['weather_descriptions'][0]
        temperature = data['current']['temperature']
        humidity = data['current']['humidity']
        wind_mph = data['current']['wind_speed']
        response = """ is {} in {} at the moment. The temperature is {} degrees, the humidity is {}% and 
            the wind speed is {} mph.""".format(
                str(condition).strip('[]\'').lower(), city, temperature, humidity, wind_mph)
        
        dispatcher.utter_message(text=f"Weather at {ent} {response}")

        return []

class ActionGetMyLocationWeather(Action):
    
    def name(self) -> Text:
        return "action_get_my_location_weather"
    
    def run(self,dispatcher:CollectingDispatcher,
        tracker: Tracker,
        domain:Dict[Text,Any]) -> List[Dict[Text,Any]]:
        
        slot_value = tracker.get_slot("location")
        data = get_weather(slot_value)
        city = data['location']['name']
        condition = data['current']['weather_descriptions'][0]
        temperature = data['current']['temperature']
        humidity = data['current']['humidity']
        wind_mph = data['current']['wind_speed']
        response = """ is {} in {} at the moment. The temperature is {} degrees, the humidity is {}% and 
            the wind speed is {} mph.""".format(
                str(condition).strip('[]\'').lower(), city, temperature, humidity, wind_mph)
        
  
        dispatcher.utter_message(text=response)
        return []

                
    