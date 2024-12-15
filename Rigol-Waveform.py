# IN WORK
# 
# Raw waveform data retrieval 
# 
# Unfinished
# 

from ds1054z import DS1054Z
import pyvisa
import matplotlib.pyplot as plt
import numpy as np

# define scope
scope = DS1054Z('169.254.131.118')
print("Connected to: ", scope.idn)

# Get the screen image
scope.stop()
scope.write(':WAV:DATA? CHAN1')  # Select channel 1
raw_data = scope.read_raw()

# Process the data
header_size = 10 # First 10 bytes are header
data = np.frombuffer(raw_data[header_size:], dtype=np.int8) 
voltage_data = (data - 128) * (scope.query(':CHAN1:SCAL?') / 25) # Convert to voltage

# Generate time axis
time_scale = float(scope.query(':TIM:SCAL?'))
time_data = np.arange(0, len(voltage_data)) * time_scale

# Plot the waveform
plt.plot(time_data, voltage_data)
plt.xlabel('Time (s)')
plt.ylabel('Voltage (V)')
plt.show()

# Close the connection
scope.close()