from datetime import datetime
import json
import os
import sqlite3
import time
from urllib.request import urlopen

from shapely.geometry import shape

RAIN_JSON_URL = "http://localhost:3000/now"
DAIRY_FARM_GEOJSON_FILE = "dairy_farm_actual.json"
RAIN_DB = "rain.db"

def init_db():
    conn = sqlite3.connect(RAIN_DB)
    c = conn.cursor()
    c.execute('''CREATE TABLE rain_data (datetime datetime, geojson text, intensity int)''')
    conn.commit()
    conn.close()
    
def main():
    # create table if doesn't exist
    try:
        init_db()
    except:
        print("db alr exists")

    with open(DAIRY_FARM_GEOJSON_FILE, "r") as read_file:
        dairy_farm = json.load(read_file)
        df_poly = shape(dairy_farm["features"][0]["geometry"])

    # every 5min, query http, write to db if rained
    while True:
        f = urlopen(RAIN_JSON_URL)
        rain_str = f.read().decode('utf-8')
        rain_json = json.loads(rain_str)

        # get curr_datetime from rain_json["id"]
        curr_datetime = datetime.strptime(str(rain_json["id"]),'%Y%m%d%H%M')
        iso_datetime = curr_datetime.isoformat(' ')
        print(iso_datetime)

        max_intensity = -1
        for feature in rain_json['features']:
            rain_poly = shape(feature['geometry'])
            rain_intensity = feature["properties"]["intensity"]
            
            rain_intersect = rain_poly.intersection(df_poly)

            if str(rain_intersect) != 'GEOMETRYCOLLECTION EMPTY':
                print(rain_intersect) 
                print(rain_intensity)
                
                if rain_intensity > max_intensity:
                    max_intensity = rain_intensity

        # write to database [iso_time, rain_json, max_intensity]
        conn = sqlite3.connect(RAIN_DB)
        c = conn.cursor()
        c.execute("INSERT INTO rain_data VALUES ('{}','{}','{}')".format(
            iso_datetime, json.dumps(rain_json), max_intensity))
        conn.commit()
        conn.close()
        print("write ok")

        time.sleep(300) # sleep 5 mins

if __name__ == "__main__":
    main()
