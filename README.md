# Unofficial-chat-gpt
- An unofficial way to access ChatGPT in your app using Browserless and selenium
- It receives an sms message, opens a headless browser, and parses html to return a response sms message to the sender.


A quick demo of what you'll get!
[![Watch the video](https://user-images.githubusercontent.com/16071943/206563542-ea661898-aa51-43f2-a948-6bb4db83fb07.png)](https://www.canva.com/design/DAFUNAixr9U/watch)

# How to install
- Make sure that python and virual environment is installed
- Clone the github repo
```
gh repo clone rdowns26/unofficial-chat-gpt
```
- Open unofficial-chat-gpt directory
```
cd unofficial-chat-gpt
```
- Create .env file for your environment variables
```
mkdir .env
```
- Add your environment variables to the .env file in the following format without the brackets
```
OPENAI_EMAIL={your open AI login email}
OPENAI_PASSWORD={your open AI login password}

# obtain a free Browserless API key by creating an account here: https://www.browserless.io/sign-up/
BROWSERLESS_KEY={your Browserless API key}

# create a free starter Twilio account and purchase a phone number, create an account here: https://www.twilio.com/try-twilio
TWILIO_NUMBER = {your purchased Twilio phone number, i.e. 15555555555}
TWILIO_ACCOUNT_SID = {your Twilio account_sid, i.e. AC2xxx...} 
TWILIO_AUTH_TOKEN = {your Twilio auth_token, i.e. 5ddxxx...} 
```
- Create a new virtual environment
```
# just once in your project directory
python3 -m venv venv

# activate the venv everytime you want to run the server
source pyenv/bin/activate
```
- Install the requirements
```
pip3 install -r requirements.txt
```
- Now run the main.py file
```
python3 main.py
```

# Enabling the Twilio webhook to talk to your flask app:
- Go to your Twilio account's active phone numbers
- Find the phone number you just created
- Go to the configure tab and scroll to the bottom
- Find the Messaging section
- Enter your app's public URL into the "A MESSAGE COMES IN WEBHOOK" section with the "/sms" endpoint added to the end (i.e. https://a6f9-2600-1700.ngrok.io/sms)

Tip: we used ngrok to create a public URL to access our local host in order to receive the webhook information from Twilio

# Inspired by
- Tarnjeet's ChatGPT api repo: https://github.com/taranjeet/chatgpt-api
- Daniel Gross' whatsapp GPT repo: https://github.com/danielgross/whatsapp-gpt

