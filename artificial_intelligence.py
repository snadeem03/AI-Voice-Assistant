import subprocess as sp
import re

result=sp.run(["netsh","wlan","show","interfaces"],capture_output=True,text=True).stdout

#We are using regular expressions here
description_match = re.search(r"Description\s+:\s+(.*)", result)

if description_match:
    description = description_match.group(1)
    print("The name of the wireless adapter is :",description.strip()) 
else:
    print("Description not found in the input string.")

physical_address_match = re.search(r"Physical address\s+:\s+(\S+)", result)

if physical_address_match:
    physical_address = physical_address_match.group(1)
    print("The MAC address of the device is : ",physical_address)  # 
else:
    print("Physical address not found in the input string.")

#finding the state :
state_match = re.search(r"State\s+:\s+(\S+)", result)

if state_match:
    state = state_match.group(1)
    print(f"You are {state} to the internet")  
else:
    print("State not found in the input string.")


#finding the name of the network :
ssid_match = re.search(r"SSID\s+:\s+(\S+)", result)

if ssid_match:
    ssid = ssid_match.group(1)
    print(f"The name of the network is {ssid}") 
else:
    print("SSID not found in the input string.")

#finding the MAC address of the router :
bssid_match = re.search(r"BSSID\s+:\s+(\S+)", result)

if bssid_match:
    bssid = bssid_match.group(1)
    print(f"The MAC address of the router is {bssid}")  
else:
    print("BSSID not found in the input string.")


#finding the security level of the network :
authentication_match = re.search(r"Authentication\s+:\s+(\S+)", result)

if authentication_match:
    authentication = authentication_match.group(1)

    if(authentication=="WPA2-Personal"):
      print(f"You are using secured network which is authenticated by {authentication}")

    else:
      print("I think you are using an in-secured network")
else:
    print("Authentication not found in the input string.")

#finding the signal strength :
signal_strength_match = re.search(r"Signal\s+:\s+(\S+)", result)

if signal_strength_match:
    signal_strength = signal_strength_match.group(1)
    print(f"Signal Strength is : {signal_strength}")  
else:
    print("Signal strength not found in the input string.")














