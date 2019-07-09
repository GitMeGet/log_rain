import datetime
import os

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
            prev_time_obj = datetime.datetime.strptime(prev_time_str, '%H%M')
            time_obj = datetime.datetime.strptime(time_str, '%H%M')
            is_sequential = (time_obj == (prev_time_obj + datetime.timedelta(minutes=5)))
        
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

def read_log_file():
    curr_time = datetime.datetime.now()
    date_base_path = str(curr_time.date())
    RAIN_LOG_FILE = "rain.log"

    # read from folders "today" and "yesterday"
    log_file_path = os.path.join(date_base_path, RAIN_LOG_FILE)
    try:
        with open(log_file_path, 'r') as f:
            logs = f.read()
    except:
        return "No rain" # if log file doesn't exist
        
    dedup = remove_dup(logs)
    seq_data = lump_sequential(dedup)
    
    ret_str = date_base_path + "\n"
    ret_str += "start_time, duration, rain_intensity\n"
    for triple in seq_data:
        ret_str += str(triple) + "\n"
        
    return ret_str
        
if __name__ == "__main__":
    ret_str = read_log_file()
    print(ret_str)