# Rigol Scope Trigger and Capture
# 
# Set up scope for statistic measurements, trigger, retrieve those measurements and save to file
# Grab screenshot using ds1054z library package CLI with OS call on executable

from ds1054z import DS1054Z

# import datetime
import time
import os

counter = 0

scope = DS1054Z('169.254.131.118')
print("Connected to: ", scope.idn)

scope.display_channel(1,1)
scope.display_channel(2,0)
scope.display_channel(3,0)
scope.display_channel(4,0)
print("Currently displayed channels: ", str(scope.displayed_channels))

scope.write(':CHAN1:COUPling DC')
scope.write(':CHAN1:INVert OFF')
scope.set_probe_ratio(1,10)
scope.set_channel_scale(1,0.5)
scope.write(':CHAN1:UNITs VOLTage')
scope.set_channel_offset(1,-1.5)
scope.write(':CHAN1:BWLimit OFF')

scope.timebase_scale = 200E-6
scope.timebase_offset = +200E-6
scope.write(':TRIGger:MODE EDGE')
scope.write(':TRIGger:EDGe:SOURce CHAN1')
scope.write(':TRIGger:EDGe:SLOPe POS')
scope.write(':TRIGger:COUPling DC')
scope.write(':TRIGger:EDGe:LEVel 1.5')
scope.write(':TRIGger:SWEep SINGle')

scope.single()

# allow time for scope to set up
time.sleep(3)

# check waiting for trigger
Status = scope.query(':TRIGger:STATus?')
print("Waiting? ", Status)

while (True):
    status = scope.query(':TRIGger:STATus?')
    if status == "STOP" :  
        # Scope triggered
        print ("triggered")
        counter += 1

        # Get measured data and display for user
        Vmax = float(scope.query(':MEASure:VMAX?'))
        Vrms = float(scope.query(':MEASure:VRMS?'))
        print(f"counter: {counter}, Vmax {Vmax:.3f}, Vrms: {Vrms:.3f}")

        # Grab screenshot
        os.system("ds1054z save-screen --overlay 0.6 169.254.131.118")
        # allow time for save before allowing re-triggering, single-mode
        time.sleep(2)

        # Trigger for next event
        scope.single()

        # Allow time for scope to set up after trigger 
        time.sleep(2)
    else:    
        # Still waiting for trigger, notify user of status
        print ("not triggered")
        time.sleep(1)

# Close the connection
scope.close()
