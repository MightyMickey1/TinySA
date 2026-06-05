from gpsdclient import GPSDClient
import csv
import time

num = 0
outFile = f'TinySA/tinySA_API/Data/output{num}.csv'
with open(outFile, 'w', newline='') as csvfile:
    fieldnames = [['Latitude', 'Longitude', 'Time']]
    writer = csv.writer(csvfile)
    writer.writerows(fieldnames)

# or as python dicts (optionally convert time information to `datetime` objects)
with GPSDClient() as client:
    while input() != 'E':
        result = client.dict_stream(convert_datetime=True, filter=["TPV"])
        # Get GPS coordinates and time
        gpsLat = next(result).get("lat", "n/a")
        gpsLong = next(result).get("lon", "n/a")
        gpsTime = next(result).get("time", "n/a")
        print("Latitude: %s" % gpsLat)
        print("Longitude: %s" % gpsLong)
        print("Time: %s" % gpsTime)

        # Write data to csv
        csvEntry = [[gpsLat, gpsLong, gpsTime]]
        with open(outFile, 'a', newline='') as csvfile:
            #fieldnames = ['Latitude', 'Longitude', 'Time']
            writer = csv.writer(csvfile)
            writer.writerows(csvEntry)

        time.sleep(10.0)