# Rigol Scope Trigger and Capture
# 
# Set up scope for statistic measurements, trigger, retrieve those measurements and save to file
# Grab screenshot using ds1054z library package CLI with OS call on executable

# Following packages are required
from ds1054z import DS1054Z
import datetime
import time
import os
import keyboard

# Function to open or creates folder
def open_or_create_folder(folder_path):
    # Opens a folder if it exist, otherwise create it.
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
     
# Prep user folder to log data
save_path = 'C:\\Users\\calve\\Desktop\\RigolData'
open_or_create_folder(save_path)

# Set counter to log number of triggers to store with data
counter = 0

# Create measurement data log file with header
# Generate filename based on the current date & time
dt = datetime.datetime.now()
filename = dt.strftime("%Y%m%d.txt")
# Create file with header info
with open(os.path.join(save_path, filename), "w") as datafile:
    datafile.write("Count, Time, Vpk2pk, Vrms\n")
    datafile.close()

# Connect with scope
scope = DS1054Z('169.254.131.118')          #Modify IP to scope addres
print("Connected to: ", scope.idn)

# Set display channels
scope.display_channel(1,1)
scope.display_channel(2,0)
scope.display_channel(3,0)
scope.display_channel(4,0)
print("Currently displayed channels: ", str(scope.displayed_channels))

# Set vertical
scope.write(':CHAN1:COUPling DC')
scope.write(':CHAN1:INVert OFF')
scope.set_probe_ratio(1,10)
scope.set_channel_scale(1,0.5)
scope.write(':CHAN1:UNITs VOLTage')
scope.set_channel_offset(1,-1.5)
scope.write(':CHAN1:BWLimit OFF')

# Set timebase
scope.timebase_scale = 200E-6
scope.timebase_offset = +200E-6
scope.write(':TRIGger:MODE EDGE')
scope.write(':TRIGger:EDGe:SOURce CHAN1')
scope.write(':TRIGger:EDGe:SLOPe POS')
scope.write(':TRIGger:COUPling DC')
scope.write(':TRIGger:EDGe:LEVel 1.5')
scope.write(':TRIGger:SWEep SINGle')

# Set acquisition single-mode
scope.single()

# allow time for scope to set up
time.sleep(3)

# Check if scope set up and waiting for trigger
Status = scope.query(':TRIGger:STATus?')
print("Waiting? ", Status)

# Continous loop to trigger, record data, and set up for next trigger
while (True):

    # Check for escape key
    if keyboard.is_pressed('esc'):
        break  

    status = scope.query(':TRIGger:STATus?')
    if status == "STOP" :  
        # Scope triggered
        print ("triggered")
        counter += 1

        # Get measured data and display for user
        Vmax = float(scope.query(':MEASure:VMAX?'))
        Vrms = float(scope.query(':MEASure:VRMS?'))
        print(f"counter: {counter}, Vmax {Vmax:.3f}, Vrms: {Vrms:.3f}")

        # Append measured data to data file
        with open(os.path.join(save_path , filename), "a") as datafile:
            datafile.write(f"{counter:4.0f}, {dt.hour:02d}.{dt.minute:02d}.{dt.second:02d}, {Vmax:.3f}, {Vrms:.3f}\n")
            datafile.close()

        # # Grab screenshot with executable  (NOT NEEDED)
        # os.system("ds1054z save-screen --overlay 0.6 169.254.131.118")

        # # Grab screenshot with ds1054z API
        bmp_image = scope.display_data
        dt = datetime.datetime.now()
        screenshot_filename = dt.strftime("%Y%m%d_%H.%M.%S.") + str(counter) + ".png"
        with open(os.path.join(save_path, screenshot_filename), 'wb') as f:
            f.write(bmp_image)
        # allow time for bitmap save before allowing scope to re-trigger
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
