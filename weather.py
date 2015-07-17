import contextlib
import json
import os
import sys
import urllib
import urllib2

from google.appengine.api import users
from google.appengine.ext import ndb

import jinja2
import webapp2


# ------------------------------------------------------------------------- #

API_KEY = "8e635b5992d237d6"

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

# ------------------------------------------------------------------------- #

# http://www.wunderground.com/weather/api/d/docs
# http://www.wunderground.com/weather/api/d/docs?d=data/hourly10day
# http://api.wunderground.com/api/8e635b5992d237d6/hourly10day/q/CA/San_Francisco.json

# e.g.
# http://api.wunderground.com/api/8e635b5992d237d6/conditions/q/CA/San_Francisco.json

def make_location(city=None, state=None, country=None,
                  zipcode=None,
                  lat=None, lng=None,
                  airport=None,
                  pws_id=None,
                  autoip=False,
                  ip_address=None):
    """
    CA/San_Francisco	US state/city
    60290	US zipcode
    Australia/Sydney	country/city
    37.8,-122.4	latitude,longitude
    KJFK	airport code
    pws:KCASANFR70	PWS id
    autoip	AutoIP address location
    autoip.json?geo_ip=38.102.136.138	specific IP address location
    """
    if autoip:
        return "autoip"
    if zipcode:
        return zipcode
    if pws_id:
        return pws_id
    if airport:
        return airport
    if ip_address:
        return "autoip.json?geo_ip={0}".format(ip_address)
    if lat and lng:
        return "{lat},{lng}".format(lat=lat, lng=lng)
    if city:
        if country:
            return "{country}/{city}".format(country=country, city=city)
        if state:
            return "{state}/{city}".format(state=state, city=city)
        # When the API location query does not produce an exact location match,
        # a results array will be present in the JSON response.
        # Each result object has an l parameter (short for link) that can be
        # used for constructing wunderground URLs:
        return city
    elif not state:
        return "NY/New_York"
    raise ValueError("Not enough information to make a location request")

def request(key,
            features="hourly10day",
            location="NY/New_York",
            fmt="json",
            settings=None):
    """
    Features:
    
    alerts	Returns the short name description, expiration time and a long text description of a severe alert - if one has been issued for the searched upon location.
    almanac	Historical average temperature for today
    astronomy	Returns the moon phase, sunrise and sunset times.
    conditions	Returns the current temperature, weather condition, humidity, wind, 'feels like' temperature, barometric pressure, and visibility.
    currenthurricane	Returns the current position, forecast, and track of all current hurricanes.
    forecast	Returns a summary of the weather for the next 3 days. This includes high and low temperatures, a string text forecast and the conditions.
    forecast10day	Returns a summary of the weather for the next 10 days. This includes high and low temperatures, a string text forecast and the conditions.
    geolookup	Returns the the city name, zip code / postal code, latitude-longitude coordinates and nearby personal weather stations.
    history	history_YYYYMMDD returns a summary of the observed weather for the specified date.
    hourly	Returns an hourly forecast for the next 36 hours immediately following the API request.
    hourly10day	Returns an hourly forecast for the next 10 days
    planner	planner_MMDDMMDD returns a weather summary based on historical information between the specified dates (30 days max).
    rawtide	Raw Tidal information for graphs
    tide	Tidal information
    webcams	Returns locations of nearby Personal Weather Stations and URL's for images from their web cams.
    yesterday	Returns a summary of the observed weather history for yesterday.
    
    
    settings (optional)
    One or more of the following settings, given as key:value pairs separated by a colon.
    Example: lang:FR/pws:0
    lang	lang code	Default: EN. Returns the API response in the specified language.
    pws	0 or 1	Default: 1 (true). Use personal weather stations for conditions.
    bestfct	0 or 1	Default: 1 (true). Use Weather Undergrond Best Forecast for forecast.
    
    query
    The location for which you want weather information. Examples:
    CA/San_Francisco	US state/city
    60290	US zipcode
    Australia/Sydney	country/city
    37.8,-122.4	latitude,longitude
    KJFK	airport code
    pws:KCASANFR70	PWS id
    autoip	AutoIP address location
    autoip.json?geo_ip=38.102.136.138	specific IP address location
    
    
    format
    json, or xml
    Output format.
    
    For JSONP, you may add ?callback=your_js_callback_function to the request URL
    
    """
    if not settings:
        settings = ""
    else:
        settings = "".join("/{key}:{value}".format(key=key, value=value)
                            for (key, value) in settings.iteritems())        
    return "http://api.wunderground.com/api/{key}/{features}{settings}/q/{location}.{fmt}".format(
        key=key,
        features=features,
        settings=settings,
        location=location,
        fmt=fmt)

# ------------------------------------------------------------------------- #

class MainPage(webapp2.RequestHandler):

    def get(self):

        output = []

        hourly_10day_url = request(API_KEY, location=make_location())
        with contextlib.closing(urllib2.urlopen(hourly_10day_url)) as fd:
            data = json.loads(fd.read())

        for fc in data['hourly_forecast']:
            output.append([fc['FCTTIME']['pretty'],
                           fc['condition'],
                           fc['temp']['english'],
                           fc['humidity']])

        self.response.write("<br>".join(", ".join(o) for o in output))

# ------------------------------------------------------------------------- #

app = webapp2.WSGIApplication([
    ('/', MainPage),
], debug=True)

# ------------------------------------------------------------------------- #



