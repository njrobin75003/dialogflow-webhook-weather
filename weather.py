from flask import Flask,request,make_response
import os,json
import pyowm
import os
import constants
import files
import cnil_open_data_manager as codm

app = Flask(__name__)
#owmapikey=os.environ.get('OWMApiKey') #or provide your key here
owmapikey="03392529d8ee503bed9526caa9cf428b"
owm = pyowm.OWM(owmapikey)

#getting and sending response to dialogflow
@app.route('/webhook', methods=['POST'])
def webhook():
    
    r = None
    req = request.get_json(silent=True, force=True)

    if (req["queryResult"]["intent"]["displayName"] == "9999-GetWeather") :
        print("Request:")
        print(json.dumps(req, indent=4))
    
        res = processWeatherRequest(req)
        res = json.dumps(res, indent=4)
        print(res)
    
        r = make_response(res)
        r.headers['Content-Type'] = 'application/json'
    
    if (req["queryResult"]["intent"]["displayName"] == "2-DataTransfer") :
        print("Request:")
        print(json.dumps(req, indent=4))
    
        res = processDataTransferRequest(req)
        res = json.dumps(res, indent=4)
        print(res)
    
        r = make_response(res)
        r.headers['Content-Type'] = 'application/json'
    
    return r

#processing the request from dialogflow
def processWeatherRequest(req):
    
    # Get weather info from Open Weather Map.
    result = req.get("queryResult")
    parameters = result.get("parameters")
    city = parameters.get("geo-city")
    observation = owm.weather_at_place(city)
    w = observation.get_weather()
    latlon_res = observation.get_location()
    lat=str(latlon_res.get_lat())
    lon=str(latlon_res.get_lon())
     
    wind_res=w.get_wind()
    wind_speed=str(wind_res.get('speed'))
    
    humidity=str(w.get_humidity())
    
    celsius_result=w.get_temperature('celsius')
    temp_min_celsius=str(celsius_result.get('temp_min'))
    temp_max_celsius=str(celsius_result.get('temp_max'))
    
    fahrenheit_result=w.get_temperature('fahrenheit')
    temp_min_fahrenheit=str(fahrenheit_result.get('temp_min'))
    temp_max_fahrenheit=str(fahrenheit_result.get('temp_max'))
   
    # The text that needs to be sent back to DialogFlow.
    speech = "Today the weather in <strong><u>" + city + "</u></strong>:\n" + "Temperature in Celsius:\nMax temp :"+temp_max_celsius+".\nMin Temp :"+temp_min_celsius+".\nTemperature in Fahrenheit:\nMax temp :"+temp_max_fahrenheit+".\nMin Temp :"+temp_min_fahrenheit+".\nHumidity :"+humidity+".\nWind Speed :"+wind_speed+"\nLatitude :"+lat+".\n  Longitude :"+lon
    
    '''
    return {
        #"speech": speech,
        #"displayText": speech,
        #"fulfillmentText": speech,
        "fulfillmentText": speech,
        "source": "dialogflow-weather-by-njrobin"
        }
        
    '''
    return {
      "fulfillmentMessages": [
        {
          "platform": "ACTIONS_ON_GOOGLE",
          "simpleResponses": {
            "simpleResponses": [
              {
                "textToSpeech": speech,
              }
            ]
          }
        },
        {
          "platform": "ACTIONS_ON_GOOGLE",
          "simpleResponses": {
            "simpleResponses": [
              {
                "textToSpeech": "Sympa les webhooks, n'est-ce pas !?! ^^",
              }
            ]
          }
        }
      ]
    }

def processDataTransferRequest(req):
    
    req = request.get_json(silent=True, force=True)
    
    resident_location_country = req["queryResult"]["parameters"]["resident-location-country"]["name"]
    transfert_location_country = req["queryResult"]["parameters"]["transfer-location-country"]["name"]

    eu_countries_reader = files.get_eu_countries_reader()
    message = codm.data_transfert_rule(eu_countries_reader, resident_location_country, transfert_location_country)

    # The text that needs to be sent back to DialogFlow.
    speech = message
    
    '''
    return {
        "fulfillmentText": speech,
        "source": "dialogflow-weather-by-njrobin"
        }
        
    '''
    return {
      "fulfillmentMessages": [
        {
          "platform": "ACTIONS_ON_GOOGLE",
          "simpleResponses": {
            "simpleResponses": [
              {
                "textToSpeech": speech,
              }
            ]
          }
        }
      ]
    }

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    print("Starting app on port %d" % port)
    app.run(debug=False, port=port, host='0.0.0.0')
