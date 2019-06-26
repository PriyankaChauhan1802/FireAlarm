import RPi.GPIO as GPIO
import time
from twilio.rest import Client
from email.mime.text import MIMEText
import smtplib
import requests
import json


channel_fire=21
GPIO.setmode(GPIO.BCM)
GPIO.setup(channel_fire, GPIO.IN)



def callback(channel):
	print('flame detected')
	call()
	email()
	sms()
	

GPIO.add_event_detect(channel_fire ,GPIO.BOTH,bouncetime=300)
GPIO.add_event_callback(channel_fire ,callback)


def call():
	
	account_sid = 'key'
	auth_token = 'token'

	client = Client(account_sid, auth_token)

	call = client.calls.create(
                        
                        to='mobile number of the receiver',
                        from_='+16507276456',
				url='https://handler.twilio.com/twiml/EHcd0d8a67a09acf325b1bf5ca14277e2f'
                    )


	print ('call has been initiated successfully')

def email():
	fromaddr = "email id of the sender"
	toaddr = "email id of the receiver"
	msg = MIMEMultipart('alternative')
	msg['From'] = fromaddr
	msg['To'] = toaddr
	msg['Subject'] = "Emergency"

	bodyLine1 = "Fire Emergency"
	bodyLine2 = ""

	msg.attach(MIMEText(bodyLine1, 'plain'))
	msg.attach(MIMEText(bodyLine2, 'plain'))

	server = smtplib.SMTP('smtp.gmail.com', 587)
	server.starttls()
	server.login("email id of the sender", "password")
	server.sendmail(fromaddr, toaddr, msg.as_string())
	print('Email has been sent')
	server.quit()

def sms():

	URL = 'https://www.way2sms.com/api/v1/sendCampaign'

	def sendPostRequest(reqUrl, apiKey, secretKey, useType, phoneNo,senderId,textMessage):
  		req_params = {
  			'apikey':apiKey,
 			'secret':secretKey,
  			'usetype':useType,
  			'phone': phoneNo,
  			'message':textMessage,
  			'senderid':senderId
  				}
  		return requests.post(reqUrl, req_params)
	
	response = sendPostRequest(URL, 'key', 'token', 'stage', 'mobile number of the receiver', 'Fire Emergency', 'Fire!	Emergency' )

	print('SMS has been sent')



while True:
	time.sleep(1)
