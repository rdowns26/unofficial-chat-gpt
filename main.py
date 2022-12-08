from flask import Flask, jsonify, request
from twilio.twiml.messaging_response import MessagingResponse
import os, time
import utils.chatgpt as chatgpt
from twilio.rest import Client

# add your own Twilio account sid and auth token to .env
account_sid = os.getenv("TWILIO_ACCOUNT_SID")
auth_token = os.getenv("TWILIO_AUTH_TOKEN")


app = Flask(__name__)


@app.route('/')
def index():
    return jsonify({"Woohoo!": "Your flask app is running"})


# webhook route for new incoming message
@app.route('/sms', methods=['POST'])
def sms():
    print ("SMS message received")
    # get incoming message
    incoming_msg = request.values.get('Body', '').lower()
    # get incoming message's sender phone number
    msg_sender = request.values.get('From', '')
    print ("message: " + str(incoming_msg) + "; from: " + str(msg_sender))
    
    # call chatbot response function
    send_chatbot_response(incoming_msg, msg_sender)
    print("ChatGPT script completed")
    return "Done"

# function to kick off chatbot util and text back when done
def send_chatbot_response(incoming_msg, msg_sender):
    # create connection in utils/chatgpt.py
    print ("Initializing Chrome driver connection")
    driver = chatgpt.create_connection(str(os.getenv("OPENAI_EMAIL")), str(os.getenv("OPENAI_PASSWORD")))

    # return a message to the sender to try again later if the ChatGPT website isn't letting user's login
    if driver == "Try again later":
        print ("ChatGPT is down, sending response to incoming message's sender")
        client = Client(account_sid, auth_token) 
        message = client.messages.create( body="ChatGPT is down, please try again later", to=str(msg_sender), from_=os.getenv("TWILIO_NUMBER"))
        print(message.sid)

    else:
        # send request to chatbot
        print ("Engaging with ChatGPT")
        response = chatgpt.ask_question(driver, incoming_msg)
        # pause for 5 seconds
        time.sleep(5)
        # close connection
        chatgpt.close_connection(driver)
        # pause for 5 seconds
        time.sleep(5)
        # send the most recent response from ChatGPT back to the sender
        client = Client(account_sid, auth_token) 
        message = client.messages.create( body=response[0], to=str(msg_sender), from_=os.getenv("TWILIO_NUMBER") )
        print ("ChatGPT response sent")
        print(message.sid)
    return driver

if __name__ == '__main__':
    app.run(debug=False) # port=os.getenv("PORT", default=5002))
