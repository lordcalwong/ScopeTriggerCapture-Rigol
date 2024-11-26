

from ds1054z import DS1054Z[savescreen,discovery]

import matplotlib.pyplot as plt
import numpy as np
import time

scope = DS1054Z('169.254.131.118')
print("Connected to: ", scope.idn)
scope.display_channel(1,1)
scope.display_channel(2,0)
scope.display_channel(3,0)
scope.display_channel(4,0)
print("Currently displayed channels: ", str(scope.displayed_channels))

scope.write(':CHAN1:COUPling DC')
scope.set_probe_ratio(1,10)
scope.set_channel_scale(1,0.5)
scope.set_channel_offset(1,-1.5)
scope.write(':CHANnel1:BWLimit OFF')
scope.write('CHANnel1:INVert OFF')

scope.timebase_scale = 200E-6
scope.timebase_offset = +200E-6

scope.write(':TRIGger:EDGe:SOURce CHAN1')
scope.write(':TRIGger:EDGe:SLOPe POS')
scope.write(':TRIGger:COUPling DC')
scope.write(':TRIGger:EDGe:LEVel 1.5')

scope.write(":WAVeform:SOURce CHAN1")
scope.write(":WAVeform:MODE NORM")
scope.write(":WAVeform:FORMat RAW")
scope.single()

# while (True):
#     Status = scope.write(':TRIGger:STATus?')
#     time.sleep(5) 
#     print("Triggered? ", str(scope.write(':TRIGger:STATus?')))
#     # if Status != 'None' :
#     #   break
chk4trig= scope.query(':TRIGger:STATus?')
print("chk4trig = ", str(chk4trig))

# # Get the horizontal and vertical, scale and offset                    
# timescale = float(scope.query(":TIM:SCAL?"))
# timeoffset = float(scope.query(":TIM:OFFS?"))
# voltscale = float(scope.query(":CHAN1:SCAL?"))
# voltoffset = float(scope.query(":CHAN1:OFFS?"))
# print("timescale= ", str(timescale), ", timeoffset= ", str(timeoffset), ", voltscale= ", str(voltscale), ", voltoffset= ", str(voltoffset))

scope.stop()

#scope.get_waveform_samples()

# As a result, a file like this will be saved to your current
# rawdata = scope.query(":WAV:DATA? CHAN1").encode('ascii')[10:]
# data_size = len(rawdata)
# print(data_size)


# plt.plot([1,2,3,4])
# plt.ylabel('some numbers')
# plt.show()


#**********END


# bmap_scope = scope.display_data
# display(Image(bmap_scope, width=800))

# Get waveform data
# scope.write(':WAV:DATA?')
# raw_data = scope.read_raw()

# # Process the raw data
# header_len = int(raw_data[1:11].decode('ascii'))
# waveform = np.frombuffer(raw_data[header_len:], dtype='int8')

# # Plot the waveform
# plt.plot(waveform)
# plt.show()

# bmap_scope = scope.display_data
# plt.plot(bmap_scope)
# plt.ylabel('some numbers')
# plt.show()

# display(Image(bmap_scope))
# scope.set_channel_scale(1, 0.5)

# DS1054Z save-data --filename samples_{ts}.txt

# from time import sleep
# from q
