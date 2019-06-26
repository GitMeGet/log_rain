import datetime
import json
import os
import time
from urllib.request import urlopen

from shapely.geometry import shape

RAIN_JSON_URL = "http://localhost:3000/now"
DAIRY_FARM_GEOJSON_FILE = "dairy_farm_actual.json"
RAIN_LOG_FILE = "rain.log"
GEOJSON_SUFFIX = "geojson"

def main():
    with open(DAIRY_FARM_GEOJSON_FILE, "r") as read_file:
        dairy_farm = json.load(read_file)
        df_poly = shape(dairy_farm["features"][0]["geometry"])

    # every 5min, query http, log intensity (to file) if rain
    while True:
        curr_time = datetime.datetime.now()
        formatted_time = curr_time.strftime('%H%M')
        print(formatted_time)
        
        f = urlopen(RAIN_JSON_URL)
        rain_str = f.read().decode('utf-8')
        rain_json = json.loads(rain_str)
        
        # log the entire geojson
        base_path = str(curr_time.date())
        if not os.path.exists(base_path):
            os.makedirs(base_path)
        
        file_path = os.path.join(base_path, formatted_time + "." + GEOJSON_SUFFIX)    
        with open(file_path, 'w+') as outfile:
            json.dump(rain_json, outfile)
            
        for feature in rain_json['features']:
            rain_poly = shape(feature['geometry'])
            rain_intensity = feature["properties"]["intensity"]
            
            rain_intersect = rain_poly.intersection(df_poly)

            if str(rain_intersect) != 'GEOMETRYCOLLECTION EMPTY':
                print(rain_intersect) 
                print(rain_intensity)
                with open(RAIN_LOG_FILE, 'a+') as f:
                    f.write(formatted_time + ", ")
                    f.write(str(rain_intensity) + "\n")

        time.sleep(300) # sleep 5 mins

if __name__ == "__main__":
    main()
