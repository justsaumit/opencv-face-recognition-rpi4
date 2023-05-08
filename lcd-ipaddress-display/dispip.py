#!/usr/bin/env python

import drivers
from time import sleep
from subprocess import check_output

display = drivers.Lcd()

try:
    # Retrieve the IP address
    IP = check_output(["hostname", "-I"]).split()[0].decode()
    print("Writing to display")
    while True:
        display.lcd_display_string("IP Address: ", 1)
        display.lcd_display_string(str(IP), 2)  # Display the IP address on the second line
except KeyboardInterrupt:
    # If there is a KeyboardInterrupt (when you press ctrl+c), exit the program and cleanup
    print("Cleaning up!")
    sleep(.4)
    display.lcd_clear()
