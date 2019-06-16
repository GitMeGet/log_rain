import datetime
import json
import time
from urllib.request import urlopen

from shapely.geometry import shape

rain_json_url = "https://rain-geojson-sg.now.sh/now"
rain_log_file = "rain.log"

with open("dairy_farm.json", "r") as read_file:
    dairy_farm = json.load(read_file)    
    df_poly = shape(dairy_farm)

def main():
    # every 5min, query http, log intensity (to file) if rain
    while True:
        curr_time = datetime.datetime.now()
        print(curr_time)

        f = urlopen(rain_json_url)
        rain_str = f.read().decode('utf-8')
        rain_json = json.loads(rain_str)
            
        for feature in rain_json['features']:
            rain_poly = shape(feature['geometry'])
            rain_intensity = feature["properties"]["intensity"]
            
            rain_intersect = rain_poly.intersection(df_poly)

            print(rain_intersect)            
            
            if str(rain_intersect) != 'GEOMETRYCOLLECTION EMPTY':
                print(rain_intensity)
                with open(rain_log_file, 'a+') as f:
                    f.write(str(curr_time) + ", ")
                    f.write(str(rain_intensity) + "\n")

        time.sleep(300) # sleep 5 mins

if __name__ == "__main__":
    main()
