# import tinySA_python (tsapython) package
from tsapython import tinySA

# create a new tinySA object    
tsa = tinySA()

# set the return message preferences 
tsa.set_verbose(True) #detailed messages
tsa.set_error_byte_return(True) #get explicit b'ERROR' if error thrown


# attempt to connect to previously discovered serial port
success = tsa.autoconnect()

# if port open, then complete task(s) and disconnect
if success == False:
    print("ERROR: could not connect to port")
else:
   
    # get current trace data on screen
    msg = tsa.data(val=2) 
    print(msg)

    # set current device ID
    msg = tsa.device_id(3) 
    print(msg)

    # get current device ID
    msg = tsa.device_id() 
    print(msg)
    
    # get device information
    msg = tsa.info() 
    print(msg)

    # pause sweeping
    msg = tsa.pause() 
    print(msg)

    # resume sweeping
    msg = tsa.resume() 
    print(msg)

    # get current battery voltage (mV)
    msg = tsa.vbat() 
    print(msg)

    tsa.disconnect()