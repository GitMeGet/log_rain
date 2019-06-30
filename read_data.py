import datetime
import os

def remove_dup(logs):
    # split by line, then comma
    tuple_list = [(t.split(",")[0], t.split(",")[1]) for t in logs.splitlines()]
    
    # remove duplicate timings
    seen = set() 
    output = [(a, b) for a, b in tuple_list 
             if not (a in seen or seen.add(a))]
    
    return output

def read_log_file():
    curr_time = datetime.datetime.now()
    date_base_path = str(curr_time.date())
    RAIN_LOG_FILE = "rain.log"

    # read from folders "today" and "yesterday"
    log_file_path = os.path.join(date_base_path, RAIN_LOG_FILE)
    with open(log_file_path, 'r') as f:
        logs = f.read()
        
    dedup = remove_dup(logs)
    
    ret_str = date_base_path + "\n"
    ret_str += "time, rain_intensity\n"
    for time, intensity in dedup:
        ret_str += time + "," + intensity + "\n"
        
    return ret_str
        
if __name__ == "__main__":
    read_log_file()
