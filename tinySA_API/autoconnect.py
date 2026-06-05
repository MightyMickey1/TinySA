from tsapython import tinySA

# Create new tinySA object
tsa = tinySA()

# Set the return message preferences
tsa.set_verbose(True)               # Detailed messages
tsa.set_error_byte_return(True)     # get explicit b'ERROR' if error thrown

# Attempt to autoconnect
found_bool, connected_bool = tsa.autoconnect()

# If port found and connected, then complete task(s) and disconnect
if connected_bool == True:
    print("Device Connected")

    msg = tsa.get_device_id()
    print(msg)

    tsa.disconnect()

else:
    print("ERROR: Could not connect to port")