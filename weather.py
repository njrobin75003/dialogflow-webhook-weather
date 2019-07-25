from flask import Flask,request,make_response
import os,json
import pyowm
import os

app = Flask(__name__)
#owmapikey=os.environ.get('OWMApiKey') #or provide your key here
owmapikey="03392529d8ee503bed9526caa9cf428b"
owm = pyowm.OWM(owmapikey)

#geting and sending response to dialogflow
@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)

    print("Request:")
    print(json.dumps(req, indent=4))
    
    res = processRequest(req)

    res = json.dumps(res, indent=4)
    print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r

#processing the request from dialogflow
def processRequest(req):
    
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
    speech = "Today the weather in " + city + ": \n" + "Temperature in Celsius:\nMax temp :"+temp_max_celsius+".\nMin Temp :"+temp_min_celsius+".\nTemperature in Fahrenheit:\nMax temp :"+temp_max_fahrenheit+".\nMin Temp :"+temp_min_fahrenheit+".\nHumidity :"+humidity+".\nWind Speed :"+wind_speed+"\nLatitude :"+lat+".\n  Longitude :"+lon
    
    '''
    return {
        #"speech": speech,
        #"displayText": speech,
        "fulfillmentText": speech,
        "source": "dialogflow-weather-by-njrobin"
        }
    '''
    return {
        "payload": {
          "google": {
            "expectUserResponse" : true,
            "richResponse": {
              "items": [
                {
                  "simpleResponse": {
                    "textToSpeech": speech,
                  }
                }
              ]
            }
          }
        }
    }
    
if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    print("Starting app on port %d" % port)
    app.run(debug=False, port=port, host='0.0.0.0')