# close raw waveform data retrieval but NO DICE! SO CLOSE!
# 

from ds1054z import DS1054Z
import numpy

# define scope
scope = DS1054Z('169.254.131.118')
print("Connected to: ", scope.idn)

# Get the screen image
scope.stop()
scope.write(":WAVeform:SOURce CHAN1")
scope.write(":WAVeform:MODE NORM")
scope.write(":WAVeform:FORMat RAW")
bmap_scope = scope.display_data

# Convert data to numpy array
img = numpy.frombuffer(bmap_scope, dtype=numpy.uint8)

plt.imshow(img)  # why doesn't this work !!!
plt.show()

# Remove header information
bmap_scope = bmap_scope[11:]

# img.shape = (360, 640)
# Create an Image object and save as PNG
image = Image.fromarray(img)
image.save("screenshot.png")

# Close the connection
scope.close()
