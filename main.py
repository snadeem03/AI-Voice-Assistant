"""

"""

# importing libraries
import speech_recognition as sr
import wikipedia as wiki
import pyttsx3 as tts3
import sys
import os
from twilio.rest import Client
import webbrowser
import subprocess as sp
import re as regular
from wordlists import shutdown_wordlist, specification_wordlist, network_info_wordlist, youtube_wordlist, chat_wordlist, \
    wikipedia_wordlist, speedtest_wordlist, time_wordlist
import speedtest as speed
import time

# ------------------------------------------------------------------------------#

# Defining global variables

owner = os.environ["OWNER"]
password = os.environ["PASSWORD_JARVIS"]

# Twilio credentials
account_sid = os.environ["TWILIO_ACCOUNT_SID"]
auth_token = os.environ["TWILIO_AUTH_TOKEN"]
verify_sid = os.environ["VERIFY_SID"]
verified_number = os.environ["VERIFIED_NUMBER"]

is_authenticated = False
attempts_remaining = 3
# ---------------------------------

# initialising the engine
engine = tts3.init(driverName='sapi5', debug=True)
engine.setProperty('rate', 150)
engine.setProperty('volume', 0.9)


# AUTHENTICATION@STEP-1
def authentication(attempts):
    excuse_message = "Apologies, but it seems you've reached the maximum number of attempts allowed at the moment. Please feel free to return after some time to continue. Thank you for your understanding."

    if attempts == 0:  # if there are no attempts remaining , program will break its execution
        engine.say(excuse_message)
        engine.runAndWait()
        print(excuse_message)
        sys.exit("Attempts Exhausted")

    engine.say("Authentication procedure process will start in couple of minutes")
    engine.runAndWait()
    print("Authentication procedure process will start in couple of minutes")

    engine.say("Please enter the name !")
    engine.runAndWait()
    entered_name = str(input("Please enter your NAME : "))

    engine.say("Please enter the password !")
    engine.runAndWait()
    entered_pass = str(input("Please enter your PASSWORD : "))

    engine.say(
        "We kindly request your patience as we undergo the necessary steps to verify your identity. Your understanding during this process is greatly appreciated.")
    engine.runAndWait()
    print("Checking...")

    # checking the credentials
    if (entered_name.capitalize() == owner.capitalize()) and (entered_pass.capitalize() == password.capitalize()):
        print("Login Successfully completed")
        engine.say("Login completed successfully.Entering into two factor verification")
        engine.runAndWait()

        print("Entering into two factor authentication.....")
        two_factor_authentication()

    else:
        print(f"Incorrect credentials , {attempts - 1} more attempts remaining ")
        engine.say(f"Incorrect credentials,you have just {attempts - 1} attempts remaining")
        attempts = attempts - 1
        authentication(attempts)


# AUTHENTICATION@STEP-2
def two_factor_authentication():
    client = Client(account_sid, auth_token)
    verification = client.verify.v2.services(verify_sid) \
        .verifications \
        .create(to=verified_number, channel="sms")

    engine.say(f"Please input the OTP that has been dispatched to the mobile number {verified_number}")
    engine.runAndWait()
    otp = input(f"Please input the OTP that has been dispatched to the mobile number {verified_number}")

    """
     here we use verifications_check.create() function that takes in two parameters 1.phone number and code entered by the user then we are storing the response from Twilio in verification_check variable and then we are again printing the status of the verfication this time if the otp entered is correct , we can see the status as approved 
    """

    verification_check = client.verify.v2.services(verify_sid) \
        .verification_checks \
        .create(to=verified_number, code=otp)

    if verification_check.status == "approved":
        print("Authentication successful , congratulations MR nadeem")
        is_authenticated = True

    else:
        print("Code incorrect , login failure")

        resend_option = input("Want to resend code ? press Y for yes N for No")
        if resend_option == "Y":
            two_factor_authentication()
        else:
            sys.exit("Shutting down due to security reasons")


def manual_config():
    # configuring the JARVIS
    available_voices = engine.getProperty('voices')
    engine.say("Do you have a preference for a female or male voice? Type fem for female and mal for male")
    engine.runAndWait()
    gender_preference = str(
        input("Do you have a preference for a female or male voice? Type fem for female and mal for male"))

    if gender_preference == "fem":
        engine.setProperty('voice', available_voices[1].id)

    engine.say(
        "The voice has now been switched to a female gender, and we're planning to introduce additional configuration options in the future. We appreciate your understanding during this process.")
    engine.runAndWait()


def speak(name):
    if not is_authenticated:
        authentication(attempts_remaining)

    engine.say(
        "Would you prefer manual configuration, or shall I proceed with the current configurations? Type man for manual config or def for default config")
    engine.runAndWait()
    will_configure = str(input(
        "Would you prefer manual configuration, or shall I proceed with the current configurations? Type man for manual config or def for default config"))

    if will_configure == "man":
        manual_config()

    engine.say(f"OK {name} ,lets have a chat... ")
    engine.say(
        f"Feel free to engage with me as though we're friends. I'm here to assist you, and you can also pitch in to help if you'd like ")
    engine.runAndWait()
    while True:
        listen(name)


# Specifications of the engine
def show_specifications():
    rate = engine.getProperty('rate')
    voice = engine.getProperty('voice')
    volume = engine.getProperty('volume')

    engine.say(f"I go by the name JARVIS, and I was crafted by {owner} with care.")
    engine.say(f"I have a voice rate of {rate} words per minute, and my unique voice identifier is {voice}.")
    engine.say(f"my volume is currently set to {volume}")
    engine.runAndWait()


def run_shutdown(name):
    engine.say(
        f"Wishing you a wonderful day and take care, {name}. Don't hesitate to reach out if you have any questions next time.")
    engine.say("Program shutting down... Bye")
    engine.runAndWait()
    sys.exit()


def interface_info():  # we will be using Regular expressions here
    engine.say("Gathering interface information on your computer")
    engine.runAndWait()
    result = sp.run(["netsh", "wlan", "show", "interfaces"], capture_output=True, text=True).stdout

    # finding the description of adapter
    description_match = regular.search(r"Description\s+:\s+(.*)", result)
    if description_match:
        description = description_match.group(1)
        engine.say(f"The name of the wireless adapter is :{description.strip()}")
        engine.runAndWait()
        print(f"The name of the wireless adapter is : {description.strip()}")
    else:
        engine.say("Sorry,cannot find the name of the adapter")
        engine.runAndWait()
        print("Cannot find the name of the adapter")

    physical_address_match = regular.search(r"Physical address\s+:\s+(\S+)", result)

    # finding the MAC address of the device
    if physical_address_match:
        physical_address = physical_address_match.group(1)
        engine.say(f"The MAC address of the device is : {physical_address}")
        engine.runAndWait()
        print(f"The MAC address of the device is : {physical_address} ")
    else:
        engine.say("Sorry,cannot find physical address of your machine")
        engine.runAndWait()
        print("Cannot find the MAC address of the device")

    # finding the state :
    state_match = regular.search(r"State\s+:\s+(\S+)", result)

    if state_match:
        state = state_match.group(1)
        engine.say(f"The machine is {state}")
        engine.runAndWait()
        print(f"The machine is {state}")
    else:
        engine.say("Sorry,cannot find state  of your machine")
        engine.runAndWait()
        print("Cannot find the state of the machine")

    # finding the name of the network :
    ssid_match = regular.search(r"SSID\s+:\s+(\S+)", result)

    if ssid_match:
        ssid = ssid_match.group(1)
        engine.say(f"The name of the network is {ssid}")
        engine.runAndWait()
        print(f"The name of the network is {ssid}")
    else:
        engine.say("Sorry,cannot find name of the network")
        engine.runAndWait()
        print("Cannot find the name of the network")

    # finding the MAC address of the router :
    bssid_match = regular.search(r"BSSID\s+:\s+(\S+)", result)

    if bssid_match:
        bssid = bssid_match.group(1)
        engine.say(f"The MAC address of the router is {bssid}")
        engine.runAndWait()
        print(f"The MAC address of the router is {bssid}")
    else:
        engine.say("Sorry,cannot find MAC address of the router")
        engine.runAndWait()
        print("Cannot find the MAC address of the router")

    # finding the security level of the network :
    authentication_match = regular.search(r"Authentication\s+:\s+(\S+)", result)

    if authentication_match:
        auth = authentication_match.group(1)

        if auth == "WPA2-Personal":
            engine.say(f"The network you are in is secured with authentication level {authentication}")
            engine.runAndWait()
            print("WPA-2 Personal")

        else:
            engine.say("I think you are inside an in-secured network")
            engine.runAndWait()
            print(auth)
    else:
        print("Cannot find the authentication and security level")
        engine.say("Sorry , cannot find authentication and security level")
        engine.runAndWait()

    # finding the signal strength :
    signal_strength_match = regular.search(r"Signal\s+:\s+(\S+)", result)

    if signal_strength_match:
        signal_strength = signal_strength_match.group(1)
        engine.say(f"The signal strength of the network is {signal_strength}")
        engine.runAndWait()
        print(f"The signal strength of the network is {signal_strength}")
    else:
        engine.say("Sorry,cannot find signal strength  of the network")
        engine.runAndWait()
        print("Cannot find the signal strength of the network")


def network_info():
    engine.say("Gathering available networks")
    engine.runAndWait()
    result = sp.run(["netsh", "wlan", "show", "networks"], capture_output=True, text=True).stdout

    # usage of regular expressions:
    pattern = r"SSID (\d+) : ([^\n]+)\s+Network type\s+: ([^\n]+)\s+Authentication\s+: ([^\n]+)\s+Encryption\s+: ([^\n]+)"
    # finding all the matches
    matches = regular.findall(pattern, result)

    engine.say(f"There are totally {len(matches)} networks available around you")
    engine.say("Let us have a look at them")
    engine.runAndWait()

    for match in matches:
        ssid_num, ssid, network_type, authentication, encryption = match
        print(f"SSID {ssid_num}:")
        engine.say(f"Network number {ssid_num}")
        print(f"  SSID: {ssid}")
        engine.say(f"Name of the network is {ssid}")
        print(f"  Network type: {network_type}")
        engine.say(f"The network type is {network_type}")
        print(f"  Authentication: {authentication}")
        engine.say(f"The security level of the network is {authentication}")
        print(f"  Encryption: {encryption}")
        engine.say(f"The encryption of the network is {encryption}")
        engine.runAndWait()
        print()


def profiles_info():
    result = sp.run(["netsh", "wlan", "show", "profiles"], capture_output=True, text=True).stdout

    pattern = r"All User Profile\s+: ([^\n]+)"

    profiles = regular.findall(pattern, result)

    engine.say(f"There are totally {len(profiles)} profiles signed in this system")
    engine.say("Lets have a look at them")
    engine.runAndWait()
    current_profile_number = 1

    # Print the extracted information
    for profile in profiles:
        engine.say(f"Profile number {current_profile_number}")
        print(f"Profile: {profile.strip()}")
        engine.say(f"Name {profile.strip()}")
        engine.runAndWait()
        current_profile_number += 1


def display_internet_info():
    engine.say(
        "We have a variety of network-related tasks, including tasks involving interface information display, available network information display, and profile information display. Which aspect would you like to focus on? Type network for network info , interface for interface info and profiles for available profiles info")
    engine.runAndWait()
    info_choice = str(input(
        "We have a variety of network-related tasks, including tasks involving interface information display, available network information display, and profile information display. Which aspect would you like to focus on? Type network for network info , interface for interface info and profiles for available profiles info"))

    if info_choice == "interface":
        interface_info()
    elif info_choice == "network":
        network_info()
    elif info_choice == "profiles":
        profiles_info()

    else:
        print("Enter the correct choice please")
        engine.say("Enter the correct choice please")
        engine.runAndWait()
        display_internet_info()


def open_youtube():
    engine.say("Opening youtube...")
    engine.runAndWait()
    webbrowser.open("https://www.youtube.com")


# todo:use beautiful soup to scrape the headlines from news websites
def open_chat():
    engine.say("Opening chat G.P.T")
    engine.runAndWait()
    webbrowser.open("https://chat.openai.com")


def wikipedia_mode(recognizer):
    engine.say("Turning on wikipedia mode...")
    engine.say("Your inquiries will be sent to the Wikipedia API, and responses will be retrieved from that source.")
    engine.runAndWait()
    print("Your inquiries will be sent to the Wikipedia API, and responses will be retrieved from that source.")
    engine.say("You can specify the topic now !")
    engine.runAndWait()

    # running an inf loop
    while True:
        with sr.Microphone() as source:
            print("You can specify the topic now")
            audio_learn = recognizer.listen(source)

            try:
                topic_specified = recognizer.recognize_google(audio_learn, language="en-in")
                engine.say(f"Go enjoy a coffee break while I look up information about {str(topic_specified)}.")
                engine.runAndWait()
                page = wiki.page(str(topic_specified))
                print(f"Searching for {str(topic_specified)} ")
                print("Title:", page.title)
                engine.say(f"Found information on {str(page.title)}")
                engine.runAndWait()
                print("Data : ", page.content[:200])
                engine.say(f"{page.content[:200]}")
                engine.runAndWait()
            except sr.UnknownValueError as e:
                print("An unknown error value has been encountered while processing your wikipedia request ")
                engine.say("An unknown value has been encountered while processing your wikipedia request")
                engine.runAndWait()


# Function to test the speed of the internet connection
def run_speedtest():
    engine.say("This might require some time, and you find it pleasant to pause for a break.")
    engine.runAndWait()
    print("This might require some time, and you find it pleasant to pause for a break.")
    # Create an instance of speedtest class
    try:
        speedtest_instance = speed.Speedtest()
        download_speed = speedtest_instance.download() / 1000000
        upload_speed = speedtest_instance.upload() / 1000000
        engine.say(f"The download speed of your internet connection is {round(download_speed, 2)} mega bits per second")
        engine.say(f"The upload speed of your internet connection is {round(upload_speed, 2)} mega bits per second")
        engine.runAndWait()
        print(f"The download speed of your internet connection is {round(download_speed, 2)} Mbps")
        print(f"The upload speed of your internet connection is {round(upload_speed, 2)} Mbps")
    except Exception as e:
        engine.say("An unforeseen error has occurred. To gather additional details, please refer to the console.")
        engine.runAndWait()
        print(e)
        engine.say("Would you like to attempt it again? Please respond with 'Y' for yes or 'N' for no.")
        option = input("Would you like to attempt it again? Please respond with 'Y' for yes or 'N' for no. : ")
        if option == "Y" or option == "y":
            run_speedtest()
        else:
            pass


def check_time():
    engine.say("Checking the time")
    engine.runAndWait()

    try:
        current_time_unformatted = time.localtime()

        # formatting and getting time
        current_day = time.strftime("%a", current_time_unformatted)
        current_month = time.strftime("%b", current_time_unformatted)
        current_date = time.strftime("%d", current_time_unformatted)
        current_time = time.strftime("%H:%M:%S", current_time_unformatted)
        current_year = time.strftime("%Y", current_time_unformatted)

        # checking the day
        day_to_speech = {
            "Thu": "Thursday",
            "Sun": "Sunday",
            "Mon": "Monday",
            "Tue": "Tuesday",
            "Wed": "Wednesday",
            "Fri": "Friday",
            "Sat": "Saturday"
        }

        if current_day in day_to_speech:
            engine.say(f"Today is {day_to_speech[current_day]}")
            engine.runAndWait()
            print(f"Today is {day_to_speech[current_day]}")
        else:
            engine.say("Invalid day code")
            engine.runAndWait()
            print("Invalid day code")
        # checking the month
        month_to_speech = {
            "Jan": "January",
            "Feb": "February",
            "Mar": "March",
            "Apr": "April",
            "May": "May",
            "Jun": "June",
            "Jul": "July",
            "Aug": "August",
            "Sep": "September",
            "Oct": "October",
            "Nov": "November",
            "Dec": "December"
        }

        if current_month in month_to_speech:
            engine.say(f"The current month is {month_to_speech[current_month]}")
            engine.runAndWait()
            print(f"The current month is {month_to_speech[current_month]}")

        else:
            engine.say("Invalid month code")
            engine.runAndWait()
            print("Invalid month code")

        # checking the date
        engine.say(f"The date is {current_date}")
        engine.runAndWait()
        print(f"The date is {current_date}")

        # checking the time
        engine.say(f"The time is {current_time}")
        engine.runAndWait()
        print(f"The time is {current_time}")

        # checking the year
        engine.say(f"The Current year is {current_year}")
        engine.runAndWait()
        print(f"The current year is {current_year}")

    except Exception as e:
        engine.say("An unforeseen error has occurred. To gather additional details, please refer to the console")
        engine.runAndWait()
        print(e)





# function to listen user commands
def listen(name):
    try:
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            print("You can speak now !!")
            engine.say("You can speak now !!")
            engine.runAndWait()
            audio = recognizer.listen(source)
            # Transcribing the audio
            recognized_text = recognizer.recognize_google(audio, language="en-in")

            # checking for shutdown
            if any(word in recognized_text for word in shutdown_wordlist):
                run_shutdown(name)
            # checking for specifications
            if any(word in recognized_text for word in specification_wordlist):
                show_specifications()
            # checking for networks
            if any(word in recognized_text for word in network_info_wordlist):
                display_internet_info()
            # checking for YouTube words
            if any(word in recognized_text for word in youtube_wordlist):
                open_youtube()
            # checking for ChatGPT words
            if any(word in recognized_text for word in chat_wordlist):
                open_chat()
            # checking for wikipedia words
            if any(word in recognized_text for word in wikipedia_wordlist):
                wikipedia_mode(recognizer)
            # checking for speedtest words
            if any(word in recognized_text for word in speedtest_wordlist):
                run_speedtest()
            # checking for the time words
            if any(word in recognized_text for word in time_wordlist):
                check_time()





            else:
                print(f"you have said {recognized_text} and i cannot process it")
                engine.say("Sorry , your request could not be processes")

    except sr.UnknownValueError as e:
        print(f"An unknown error has been occurred {e}")
        engine.say(f"An unknown value error has been occurred,for more details check for the stderr")
        engine.runAndWait()


def ListAllAvailableVoices():
    engine.say("Listing all the available voices ...")
    engine.runAndWait()

    voices = engine.getProperty('voices')
    print(voices[1])
    print(voices[0])


if __name__ == '__main__':
    user_name = str(input("USER-NAME PLEASE"))
    speak(user_name)
