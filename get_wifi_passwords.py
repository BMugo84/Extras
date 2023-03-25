# Import the subprocess module to use system commands
import subprocess

# Import the re module for regular expressions
import re

# Run the netsh command to get the list of wireless network profiles
command_output = subprocess.run(["netsh", "wlan", "show", "profiles"], capture_output=True).stdout.decode()

# Use regex to find the profile names
profile_names = (re.findall("All User Profile     : (.*)\r", command_output))

# Create an empty list to store the wireless network profiles
wifi_list = list()

# Loop through each profile name
if len(profile_names) != 0:
    for name in profile_names:
        # Create a dictionary to store the wireless network profile information
        wifi_profile = {}
        
        # Run the netsh command to get the profile information
        profile_info = subprocess.run(["netsh", "wlan", "show", "profile", name], capture_output=True).stdout.decode()
        
        # Check if the security key is absent. If it is, skip to the next profile name
        if re.search("Security key           : Absent", profile_info):
            continue
        else:
            # Store the profile name as the SSID in the wifi_profile dictionary
            wifi_profile["ssid"] = name
            
            # Run the netsh command to get the profile password information
            profile_info_pass = subprocess.run(["netsh", "wlan", "show", "profile", name, "key=clear"], capture_output=True).stdout.decode()
            
            # Use regex to find the password
            password = re.search("Key Content            : (.*)\r", profile_info_pass)
            
            # If the password is None, store None in the wifi_profile dictionary. Otherwise, store the password.
            if password == None:
                wifi_profile["password"] = None
            else:
                wifi_profile["password"] = password[1]
            
            # Add the wifi_profile dictionary to the wifi_list list
            wifi_list.append(wifi_profile) 

# Loop through each wifi profile in the wifi_list list and print its information
for x in range(len(wifi_list)):
    print(wifi_list[x])
