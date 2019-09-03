from datetime import datetime, timedelta
import os
import sqlite3

RAIN_DB = "rain.db"

def remove_dup(logs):
    """ Remove duplicate timings, only keep highest intensity for each timing
        input: string
        output: list of (time, intensity) tuples
    """

    # split by line, then comma
    tuple_list = [(t.split(",")[0], t.split(",")[1]) for t in logs.splitlines()]
        
    dedup = list()
    curr_time = None
    curr_max = None
    for time, intensity in tuple_list:
        intensity = int(intensity)
        
        if curr_time == None and curr_max == None:
            curr_time = time
            curr_max = intensity
        elif curr_time == time and intensity > curr_max:
            curr_max = intensity
        elif time != curr_time:
            dedup.append((curr_time, curr_max))
            curr_time = time
            curr_max = intensity
    dedup.append((curr_time, curr_max))

    return dedup

def lump_sequential(dedup):
    """ Lump sequential data together
        input: list of (time, intensity) tuples
        output: list of (start_time, duration, average_intensity) triples
    """

    prev_time_str = None
    triple_list = list()
    for tuple in dedup:        
        time_str = tuple[0]
        time_int = int(time_str)
        intensity = int(tuple[1])
        
        if prev_time_str != None:
            prev_time_obj = datetime.strptime(prev_time_str, '%H%M')
            time_obj = datetime.strptime(time_str, '%H%M')
            is_sequential = (time_obj == (prev_time_obj + timedelta(minutes=5)))
        
        if prev_time_str == None or not is_sequential:
            triple_list.append((time_str, 5, intensity))
        else:
            prev_start_time = triple_list[-1][0]
            prev_time_period = triple_list[-1][1]
            prev_intensity = triple_list[-1][2]
            
            average_intensity = ((prev_intensity * prev_time_period//5) + intensity) / (prev_time_period//5 + 1)
                        
            triple_list[-1] = (prev_start_time, prev_time_period + 5, average_intensity)
        prev_time_str = time_str
            
    return triple_list

def count_intervals(logs):
    a = b = c = 0
    for time, intensity in logs:
        if intensity in range(0,32):
            a += 1
        elif intensity in range(33,66):
            b += 1
        elif intensity in range(67,100):
            c += 1

    return (a,b,c)

def read_log_file(hours_ago=8):
    to_time = datetime.now().isoformat(' ', 'seconds')
    from_time = (datetime.now() - timedelta(hours=hours_ago)).isoformat(' ', 'seconds')

    conn = sqlite3.connect(RAIN_DB)
    c = conn.cursor()
    c.execute("""SELECT datetime, intensity
from [rain_data]
where intensity != -1 AND datetime >= '{}' AND datetime < '{}' """.format(from_time, to_time))
    logs = c.fetchall()
    
    a,b,c = count_intervals(logs)
    heavy_rain_hours = c * 5
    
    ret_str = "last {} hrs, {} mins of heavy rain\n".format(hours_ago, heavy_rain_hours)

    print(to_time)
    print(from_time)
    print(logs)
    print(c)

    return ret_str
        
if __name__ == "__main__":
    ret_str = read_log_file()
    print(ret_str)