# import tinySA_python (tsapython) package
from tsapython import tinySA

# GPS conversion from JSON to Lat/Long
from gpsdclient import GPSDClient

# imports
import numpy as np
import matplotlib.pyplot as plt
import time
import csv

def convert_data_to_arrays(start, stop, pts, data):
    # using the start and stop frequencies, and the number of points, 

    freq_arr = np.linspace(start, stop, pts)    # note that the decimals might go out to many places. 
                                                # you can truncate this because it’s only used 
                                                # for plotting in this example

    # As of the Jan. 2024 build in some data returned with SWEEP or SCAN calls there is error data.  
    # https://groups.io/g/tinysa/topic/tinasa_ultra_sweep_command/104194367  
    # this shows up as "-:.000000e+01".
    # TEMP fix - replace the colon character with a -10. This puts the 'filled in' points around the noise floor.
    # more advanced filtering should be applied for actual analysis.
    data1 =bytearray(data.replace(b"-:.0", b"-10.0"))
    
    # get both values in each row returned (for reference)
    #data_arr = [list(map(float, line.split())) for line in data.decode('utf-8').split('\n') if line.strip()] 
   
    # get first value in each returned row
    data_arr = [float(line.split()[0]) for line in data1.decode('utf-8').split('\n') if line.strip()]

    return freq_arr, data_arr

def dBm_at_freq(start, stop, pts, outmask):
    # scan
    data_bytes = tsa.scan(start, stop, pts, outmask)

    #print(data_bytes)

    tsa.resume() #resume so screen isn't still frozen

    # convert data to 2 arrays
    freq_arr, data_arr = convert_data_to_arrays(start, stop, pts, data_bytes)

    #sigPower = data_arr[np.where(freq_arr == sigFreq)[0][0]]

    peakPower = np.max(data_arr)
    peakFreq = freq_arr[np.argmax(data_arr)]

    # plot
    # plt.plot(freq_arr, data_arr)
    # plt.xlabel("Frequency (Hz)")
    # plt.ylabel("Measured Data (dBm)")
    # plt.title("tinySA Scan Plot")
    # plt.show()

    return peakPower, peakFreq

# create a new tinySA object    
tsa = tinySA()

# set the return message preferences 
tsa.set_verbose(True) #detailed messages
tsa.set_error_byte_return(True) #get explicit b'ERROR' if error thrown

# attempt to autoconnect
found_bool, connected_bool = tsa.autoconnect()

# if port closed, then return error message
if connected_bool == False:
    print("ERROR: could not connect to port")
else: # if port found and connected, then complete task(s) and disconnect

    # set scan values
    start = int(3.59e9)
    stop = int(3.6e9)
    pts = 201           # sample points
    outmask = 2         # get measured data (y axis)
    #sigFreq = int(2.4e9) # Frequency of desired signal
    avg = 5             # Number of samples to average between
    sampleTime = 1.0   # Time between samples

    # Set up csv
    num = 2
    outFile = f'TinySA/tinySA_API/Data/output{num}.csv'
    fieldnames = [['Latitude', 'Longitude', 'Time', 'Peak Power [dBm]', 'Peak Frequency [Hz]']]
    with open(outFile, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(fieldnames)

    # or as python dicts (optionally convert time information to `datetime` objects)
    with GPSDClient() as client:
        while True:
            result = client.dict_stream(convert_datetime=True, filter=["TPV"])
            # Get GPS coordinates and time
            gpsLat = next(result).get("lat", "n/a")
            gpsLong = next(result).get("lon", "n/a")
            gpsTime = next(result).get("time", "n/a")
            print("Latitude: %s" % gpsLat)
            print("Longitude: %s" % gpsLong)
            print("Time: %s" % gpsTime)
            
            # Take <avg> samples and average the power and frequency of the peak
            peakPowerAvgTotal = 0
            peakFreqAvgTotal = 0
            for sample in range(avg):
                peakPower, peakFreq = dBm_at_freq(start, stop, pts, outmask)
                peakPowerAvgTotal = peakPower + peakPowerAvgTotal
                peakFreqAvgTotal = peakFreq + peakFreqAvgTotal
            
            peakPowerAvg = peakPowerAvgTotal / avg
            peakFreqAvg = peakFreqAvgTotal / avg
            #print(f'Power at {sigFreq/1e9} GHz: {sigPower} dBm')
            print(f'Peak power is {peakPowerAvg} dBm at {peakFreqAvg/1e9} GHz')
            
            # Write data to csv
            csvEntry = [[gpsLat, gpsLong, gpsTime, peakPower, peakFreq]]
            with open(outFile, 'a', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerows(csvEntry)

            time.sleep(sampleTime)

    tsa.disconnect()