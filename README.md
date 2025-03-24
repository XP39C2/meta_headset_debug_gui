# meta_headset_debug_gui
This is a simple script made during my time at META for troubleshooting META's andoid based VR headsets.

A Python GUI tool built with tkinter to help you manage and troubleshoot Meta Quest headsets using ADB commands. The application allows you to:

    Update device status and battery level

    Reboot the headset

    Launch scrcpy for screen mirroring

    Display device logs

    Open an interactive ADB shell

    Run hardware check commands (Properties, Battery, Sensors, Camera, Display) on the selected device

    Save ADB output to your Desktop

Features

    Device Management:
    List connected devices and select one to target for ADB commands.

    Hardware Diagnostics:
    Use friendly-named commands to run diagnostics on the headset (e.g., checking properties, battery, sensors, etc.).

    Screen Mirroring:
    Launch scrcpy to mirror the headset screen on your PC.

    Interactive ADB Shell:
    Open a new command prompt window with an interactive ADB shell.

    Output Logging:
    Save the output from various commands to a file on your Desktop.

Requirements

    Python 3.x

    Standard Python libraries: tkinter, subprocess, os, datetime

    ADB (Android Debug Bridge) installed and accessible in your system's PATH

    scrcpy installed (update the path in the code if necessary)
