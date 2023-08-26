"""


#1 pyttsx3 is cross-platform tts engines ,we need to use init() function to get a
new instance of engine it takes 2 params :
1.drivername=either sapi5(windows),NSSS(macos),espeak(other platforms) it defaultly
chooses best drivers if we donot provide with drivername
2.debug=True/False this is also default param ,generally set to True

SPEECH RELATED SETTINGS :
using Set property we can set various properties of the engine like setting the
voice of the engine ,rate ,volume etc
and using getProperty function we can get all the currently set properties for the engine

Other modules used :
Speech_recognition : used to recognise our voice
wikipedia :used to fetch data from the wikipedia
openai:used to power our assistant using AI

Speech Recognition:
The Recognizer class in the speech_recognition (sr) package is used for working with audio data, particularly for speech recognition tasks.we use various speech recognition  engines like bing , google etc to recognise the speech
The Recognizer class provides methods to capture audio from various sources, such as a microphone or an audio file, and then transcribe that audio into text.


r.listen():Purpose : captures audio data from the specified source
           params:source ex:microphone,audiofile
           return value:returns audio data class that can be processed by other engines


Before our JARVIS does anything for the user , the user needs to be authenticated
and authorized by the JARVIS,inorder to do that we use authentication() function the assitant does not speak up until successful authentication

OTP VERIFICATION SYSTEM:
We are going to implement a OTP verification system as a part of our authentication process.

Purpose for OTP verification system:
It adds an extra layer of security for our application and prevents attackers from phishing.

Modules :
Twilio : Twilio module helps you to integrate communication functionalities like SMS, MMS, phone calls, and verification right into your application. It has a cloud-based infrastructure along with amazing features such as number provisioning, message templates, and call recording.

Random: it is a in-built module in py used to generate pseudo random numbers that serve as OTP numbers

Twilio : here we are importing a particular class called <Client> from twilio.rest which gives access to twilio's rest API

After importing twilio's Client , we need to define some credentials of Twilio API , so that we can use those credentials to send OTP's ,the credentials are as follows : 1.Account sid
              2.Auth token
              3.verified phone number
              4.verified sid

These 4 credentials are used to authenticate with the twilio REST API











"""

# importing libraries----------
import speech_recognition as sr  # for recognizing the speech
import openai as ai  # for AI purpose
import wikipedia as wiki  # for searching a topic
import pyttsx3 as tts3  # for text to speech conversion
import sys
import os
from twilio.rest import Client  # OTP authentication
import webbrowser
import subprocess as sp
import re as regular
import speedtest_cli as sp

# -----------------------------#

# Defining global variables-----------------

# These variables are used for authentication puroses
owner = os.environ["OWNER"]  # fetches the env variable named OWNER from global env variables
password = os.environ["PASSWORD_JARVIS"]  # fetches the env variable named PASSWORD_JARVIS from global env variables

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


def authentication(attempts_remaining):
    if attempts_remaining == 0:  # if there are no attempts remaining , program will break its execution
        sys.exit("Attempts Exhausted")

    print("please proceed with the process of authentication...")
    print("We will be asking some basic questions like name and password ")
    entered_name = input("Please enter your NAME : ")
    entered_pass = input("Please enter your PASSWORD")

    # checking the credentials
    if (entered_name.capitalize() == owner.capitalize()) and (entered_pass.capitalize() == password.capitalize()):
        print("Login partially successfull")
        print("Entering into two factor authentication.....")
        two_factor_authentication()

    else:
        print(f"Incorrect credentials , {attempts_remaining - 1} more attempts remaining ")
        attempts_remaining = attempts_remaining - 1
        authentication(attempts_remaining)

    # two  factor authentication - OTP verification


def two_factor_authentication():
    # creating an twilio client instance using Client() constructor from Client class.So this clientm instance is used to interact with the Client REST API to send SMS,make Calls,manage phone numbers.it takes 2 parameters
    # account security identifier and authentication token.Return value -client instance:

    client = Client(account_sid, auth_token)
    # After creating a client instance we need to use Twilio Verify service to send an OTP and verify that OTP.For this we will use the verify_sid which we have stored in env variables.The .verifications.create() method initiates the verification process.This verifications.create() method takes in 2 parameters to_phonenumber and channel.we will fetch the phone number from the env variables and the communication channel would be SMS in our case.

    # various other options for the channel :
    """
    1.Call ("call"): Twilio can make an automated phone call to the user's phone number and read out the verification code using text-to-speech technology.
    2.Email ("email"): Twilio can send the verification code to the user's email address.
    3.WhatsApp ("whatsapp"): You can send the verification code to the user's WhatsApp account.
    4.Push ("push"): Twilio can send a push notification to the user's mobile app, prompting them to verify their phone number.
    5.Facebook messenger and Google RCS(rich communication services)
    """
    # The response from the twilio is stored as a variable named <verification>
    verification = client.verify.v2.services(verify_sid) \
        .verifications \
        .create(to=verified_number, channel="sms")
    print(f"The verification status is {verification.status}")  # This would be obviously pending

    print(f"Please check your mobile number {verified_number} and enter the OTP")
    otp = input("OTP PLEASE....")

    """
    After user enters OTP , we need to  verify whether the OTP entered is correct or not , for this we are going to use Twilio OTP verification_checks procedure . here we use verifications_check.create() function that takes in two parameters 1.phone number and code entered by the user then we are storing the response from Twilio in verification_check variable and then we are again printing the status of the verfication this time if the otp entered is correct , we can see the status as approved 
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


def run_speedtest():
    try:
        speedtest_obj=sp.Speedtest()
        server=speedtest_obj.get_best_server()

        download_speed=speedtest_obj.download()/1000000
        upload_speed=speedtest_obj.upload()/1000000
        server_info=f"The best server {server['host']} is found at {server['country']}"
        return server_info,download_speed,upload_speed

    except speed.ConfigRetrievalError:
        print("Failed to retrieve configuration. Please check your internet connection")

    except speed.NoMatchedServers:
        print("No servers found,please try after sometime")



    
    


def speak(name):
    if not is_authenticated:
        authentication(attempts_remaining)

    # configuring the JARVIS
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)

    engine.say(f"I would appreciate your patience for following the time taking"
               f"authentication procedure  ")
    engine.say(f"OK {name} ,how are you ?")
    engine.say(f"How can i help you ?")
    engine.runAndWait()
    while True:
        listen()


# this function is used to listen the user commands,we are going to use speechrecognition here
def listen():
    recognizer = sr.Recognizer()  # creating an instance of recognizer class

    # capturing audio from microphone
    with sr.Microphone() as source:
        print("I am ready,please speak up!!")
        audio = recognizer.listen(source)

    # transcribing audio to text
    try:
        recognized_text = recognizer.recognize_google(audio, language="en-in")

        shutdown_wordlist = ["power off", "shut", "turn off", "deactivate", "cease", "halt", "terminate", "end", "stop"]
        if any(word in recognized_text for word in shutdown_wordlist):
            engine.say("Program shutting down...")
            engine.runAndWait()
            sys.exit()

        specifications_wordlist = ["specifications", "capabilities", "yourself"]
        if any(word in recognized_text for word in specifications_wordlist):
            specifications()


        if str(recognized_text.lower()).find("Speedtest")!=1:
            engine.say("Running speed test..Please wait ")
            engine.runAndWait()
            info,downSpeed,upSpeed=run_speedtest()
            engine.say(info)
            engine.say(f"The download speed is {downSpeed} megabits per second")
            engine.say(f"The upload speed is {upSpeed} megabits per second")
            engine.runAndWait()



        if str(recognized_text.lower()).find("network information") != -1:
            engine.say("Gathering network information...")
            engine.runAndWait()
            result = sp.run(["netsh", "wlan", "show", "interfaces"], capture_output=True, text=True).stdout

            # We are using regular expressions here
            description_match = regular.search(r"Description\s+:\s+(.*)", result)

            if description_match:
                description = description_match.group(1)
                engine.say(f"The name of the wireless adapter is :{description.strip()}")
                engine.runAndWait()
            else:
                engine.say("Sorry,cannot find the name of the adapter")
                engine.runAndWait()

            physical_address_match = regular.search(r"Physical address\s+:\s+(\S+)", result)

            if physical_address_match:
                physical_address = physical_address_match.group(1)
                engine.say(f"The MAC address of the device is : {physical_address}")
                engine.runAndWait()
            else:
                engine.say("Sorry,cannot find physical address of your machine")
                engine.runAndWait()

            # finding the state :
            state_match = regular.search(r"State\s+:\s+(\S+)", result)

            if state_match:
                state = state_match.group(1)
                engine.say(f"The machine is {state}")
                engine.runAndWait()
            else:
                engine.say("Sorry,cannot find state  of your machine")
                engine.runAndWait()

            # finding the name of the network :
            ssid_match = regular.search(r"SSID\s+:\s+(\S+)", result)

            if ssid_match:
                ssid = ssid_match.group(1)
                engine.say(f"The name of the network is {ssid}")
                engine.runAndWait()
            else:
                engine.say("Sorry,cannot find name of the network")
                engine.runAndWait()

            # finding the MAC address of the router :
            bssid_match = regular.search(r"BSSID\s+:\s+(\S+)", result)

            if bssid_match:
                bssid = bssid_match.group(1)
                engine.say(f"The mac address of the router is {bssid}")
                engine.runAndWait()
            else:
                engine.say("Sorry,cannot find MAC address of the router")
                engine.runAndWait()

            # finding the security level of the network :
            authentication_match = regular.search(r"Authentication\s+:\s+(\S+)", result)

            if authentication_match:
                authentication = authentication_match.group(1)

                if (authentication == "WPA2-Personal"):
                    engine.say(f"The network you are in is secured with authentication level {authentication}")
                    engine.runAndWait()

                else:
                    engine.say("I think you are inside an in-secured network")
                engine.runAndWait()
            else:
                print("Authentication not found in the input string.")

            # finding the signal strength :
            signal_strength_match = regular.search(r"Signal\s+:\s+(\S+)", result)

            if signal_strength_match:
                signal_strength = signal_strength_match.group(1)
                engine.say(f"The signal strength of the network is {signal_strength}")
                engine.runAndWait()
            else:
                engine.say("Sorry,cannot find signal strength  of the network")
                engine.runAndWait()

        if str(recognized_text.lower()).find("open youtube") != -1:
            engine.say("Opening youtube...")
            engine.runAndWait()
            webbrowser.open("https://www.youtube.com")

        if str(recognized_text.lower()).find("open chat") != -1:
            engine.say("Opening chatGPT...")
            engine.runAndWait()
            webbrowser.open("https://chat.openai.com/?model=text-davinci-002-render-sha")

        # Using wikipedia library to open specific content in wikipedia.This library allows you to access Wikipedia articles and retrieve information about a particular topic.

        if str(recognized_text.lower()).find("learning mode") != -1:

            engine.say("Turning on learning mode ....")
            engine.say("Please specify the topic you want to learn ")
            engine.runAndWait()
            while True:
                with sr.Microphone() as source:
                    print("Feel free to ask questions")
                    audio_learn = recognizer.listen(source)
                    try:
                        topic_specified = recognizer.recognize_google(audio_learn, language="en-in")
                        # if str(topic_specified) == "artificial intelligence":
                        #     engine.say("artificial intelligence")
                        #     engine.runAndWait()
                        #     print("artificial intelligence loading")
                        page = wiki.page(str(topic_specified))
                        print(f"Searching for {str(topic_specified)} ")
                        print("Title:", page.title)
                        print("Summary:", wiki.summary(topic_specified))
                        print("Full Text:", page.content[:200])

                        # print("speak up clearly")
                        # engine.say("Cannot hear your voice nadeem")
                        # engine.runAndWait()
                        # print(f"you have said {str(topic_specified)}")



                    except sr.UnknownValueError() as e:
                        print("cannot recognize your voice , speak up clearly")
                        engine.say("Cannot hear your voice nadeem")
                        engine.runAndWait()
                        print(f"you have said {str(topic_specified)}")

                    except wiki.exceptions.PageError as e:
                        print(f"Page not found and error is {e}")

                    except wiki.exceptions.DisambiguationError as e:
                        print("disambiguations error occured ")















        else:
            print(f"you have said {recognized_text} ")

    except sr.UnknownValueError as uv_error:
        print(uv_error)
        print("Please speak loudly or clearly")
        engine.say(f"Sorry for the inconvenience {owner},can you speak clearly")
        engine.runAndWait()

    except sr.RequestError as re:
        print(f"Bad request {re}")
        engine.say("Something went wrong in there .. please try again")
        engine.runAndWait()


# Specifications of the engine
def specifications():
    rate = engine.getProperty('rate')
    voice = engine.getProperty('voice')
    volume = engine.getProperty('volume')

    engine.say(f"My name is JARVIS and i have been developed by {owner}")
    engine.say(f"My specifications are : my voice rate is {rate} words per minute. My voice I.D is {voice}")
    engine.say(f"my volume is currently set to {volume}")
    engine.runAndWait()


def ListAllAvailableVoices():
    engine.say("Listing all the available voices ...")
    engine.runAndWait()

    voices = engine.getProperty('voices')
    print(voices[1])
    print(voices[0])


if __name__ == '__main__':
    speak("nadeem")
