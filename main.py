import template
import template1
import os
import sys
import json
from bs4 import BeautifulSoup
import random
import requests
from flask import Flask, request

app = Flask(__name__)

PAGE_TOKEN = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
VERIFY_TOKEN = "hello"
welcome = ["hi", "hey", "hello"]

@app.route('/', methods=['GET'])
def verify():
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        if not request.args.get("hub.verify_token") == VERIFY_TOKEN:
            return "Verification token mismatch", 403
        return request.args["hub.challenge"], 200

    return "Working", 200


@app.route('/', methods=['POST'])
def webook():

    # endpoint for processing incoming messaging events

    data = request.get_json()
    print data
    log(data)  # you may not want to log every incoming message in production, but it's good for testing

    if data["object"] == "page":

        for entry in data["entry"]:
            for messaging_event in entry["messaging"]:

				if messaging_event.get("message"):  # someone sent us a message

					print '?'*20

					print messaging_event
					print '?'*20

					sender_id = messaging_event["sender"]["id"]        # the facebook ID of the person sending you the message
					recipient_id = messaging_event["recipient"]["id"]
                                        print messaging_event

					message_text = messaging_event["message"]["text"]
                    # the message's text

                                        if message_text in welcome:
                                            send_typing(sender_id)
                                            send_message(sender_id,"Welcome to Travel Guide! Explore Rajasthan with just one tap.")
                                            send_quick_reply(sender_id)
                                        elif message_text == 'Hotels':
                                            send_typing(sender_id)
                                            send_message(sender_id,"Which city do you want?")
                                            hotels=template.hotel('jaipur')
                                            if len(hotels)>5:
                                                send_message(sender_id,hotels[0])
                                                send_message(sender_id,hotels[1])
                                                send_message(sender_id,hotels[2])
                                                send_message(sender_id,hotels[3])
                                                send_message(sender_id,hotels[4])
                                                send_quick_reply(sender_id)
                                            else:
                                                send_typing(sender_id,hotels[0])
                                        if message_text == "Tourist Attraction":
                                            send_typing(sender_id)
                                            places=template1.place('jaipur')
                                            if len(places)>5:
                                                send_message(sender_id,places[0])
                                                send_message(sender_id,places[1])
                                                send_message(sender_id,places[2])
                                                send_message(sender_id,places[3])
                                                send_message(sender_id,places[4])
                                                send_quick_reply(sender_id)
                                            else:
                                                send_typing(sender_id,attractions[0])



				if messaging_event.get("delivery"):
					pass

				if messaging_event.get("optin"):  # optin confirmation
					pass

				if messaging_event.get("postback"):  # user clicked/tapped "postback" button in earlier message
					msg = messaging_event["postback"]['payload']
					send_id = messaging_event["sender"]['id']

					
				if msg == "Travel":
				    send_msg = "Travel Guide is your personal guide assistant which gives you all information about travel and tourism."
				    send_message(send_id, send_msg)
                                elif msg == "start_button":
                                    send_msg =(send_id,"Hello " + str(name.replace("_"," ")) + " \n" + "Welcome to Travel Guide, your travel assistant to give the information you want." )
				elif msg == "yash":
				    send_msg = "This project was done by Shrey Patel and Yash Shah at the rajasthan hackathon 4.0"
                                    send_message(send_id, send_msg)



    return "ok", 200


def send_message(recipient_id, message_text):

    log("sending message to {recipient}: {text}".format(recipient=recipient_id, text=message_text))

    params = {
        "access_token": PAGE_TOKEN
    }
    headers = {
        "Content-Type": "application/json"
    }
    data = json.dumps({
        "recipient": {
            "id": recipient_id
        },
        "message": {
            "text": message_text
        }
    })
    r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)
    if r.status_code != 200:
        log(r.status_code)
        log(r.text)


def send_typing(recipient_id):

	params = {
        "access_token": PAGE_TOKEN
    }
	headers = {
        "Content-Type": "application/json"
    }
	data = json.dumps({
        "recipient": {
            "id": recipient_id
        },
        "sender_action":"typing_on"
    })
	r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)



def send_quick_reply(recipient_id):


	params = {
        "access_token": PAGE_TOKEN
    }
	headers = {
        "Content-Type": "application/json"
    }
	data = json.dumps({
        "recipient": {
            "id": recipient_id
        },
        "message": {
						"text":'Services we provide.',
						"quick_replies":[
							{
								"content_type":"text",
								"title":"Tourist Attraction",
								"payload":"next"
							},
                            {
								"content_type":"text",
								"title":"Hotels",
								"payload":"next"
							},
                            {
								"content_type":"text",
								"title":"Nearby Hospitals",
								"payload":"next"
							},
                            {
								"content_type":"text",
								"title":"Emergency Numbers",
								"payload":"next"
							},


						]
					}
    })

	r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)



#menu
def per_menu():
	params = {
		"access_token": PAGE_TOKEN
	}
	headers = {
		"Content-Type": "application/json"
	}

	data = json.dumps({
			"setting_type" : "call_to_actions",
			"thread_state" : "existing_thread",
			"call_to_actions":[
				{
					"type":"postback",
					"title":"Travel Guide",
					"payload":"Travel"
				},
				{
					"type":"postback",
					"title":"Created by Blue Wizzards",
					"payload":"yash"
				}
			]
		})
	r = requests.post("https://graph.facebook.com/v2.6/me/thread_settings", params=params, headers=headers, data=data)

#menu
def start_button():
	params = {
		"access_token": PAGE_TOKEN
	}
	headers = {
		"Content-Type": "application/json"
	}

	data = json.dumps({
			"setting_type" : "call_to_actions",
			"thread_state" : "new_thread",
			"call_to_actions":[
				{
					"payload":"start_button"
				}
			]
		})
	r = requests.post("https://graph.facebook.com/v2.6/me/thread_settings", params=params, headers=headers, data=data)


per_menu()
start_button()



def log(message):  # simple wrapper for logging to stdout on heroku
	print "-"*10
	# print str(message)
	sys.stdout.flush()

if __name__ == '__main__':
    app.run(debug=True,port=80)
