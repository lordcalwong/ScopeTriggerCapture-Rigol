from ds1054z import DS1054Z

scope = DS1054Z('169.254.131.118')  # Replace with your oscilloscope's IP address

# Save the screenshot
bmp_image = scope.display_data
scope.close()

with open('screenshot.png', 'wb') as f:
    f.write(bmp_image)