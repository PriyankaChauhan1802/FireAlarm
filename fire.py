import RPi.GPIO as GPIO
import time
from twilio.rest import Client
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
import requests
import json


channel_fire=21
channel_sound=16
GPIO.setmode(GPIO.BCM)
GPIO.setup(channel_sound,GPIO.OUT)
GPIO.setup(channel_fire, GPIO.IN)
GPIO.output(channel_sound,GPIO.LOW)

account_sid = 'ACabc6bb44978a11d1d24fc21fdae4f3c3'
auth_token = '2efa0053be19e08a1a3fe94c4a113e9d'

def callback(channel):
	print('flame detected')
	call()
	email()
	sms()
	#soundon()

GPIO.add_event_detect(channel_fire ,GPIO.BOTH,bouncetime=300)
GPIO.add_event_callback(channel_fire ,callback)


def soundon():
	GPIO.output(channel_sound,GPIO.HIGH)
def soundoff():
	GPIO.output(channel_sound,GPIO.LOW)


def call():
	
	account_sid = 'ACabc6bb44978a11d1d24fc21fdae4f3c3'
	auth_token = '2efa0053be19e08a1a3fe94c4a113e9d'

	client = Client(account_sid, auth_token)

	call = client.calls.create(
                        
                        to='+919930044490',
                        from_='+16507276450',
				url='https://handler.twilio.com/twiml/EHcd0d8a67a09acf325b1bf5ca14277e2f'
                    )


	print ('call has been initiated successfully')

def email():
	fromaddr = "test18021993@gmail.com"
	toaddr = "kratikagulati95@gmail.com"
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
	server.login("test18021993@gmail.com", "Priyanka@123")
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
	
	response = sendPostRequest(URL, 'FHRTZ66XUNRWU3N3GYL6GHPV63X5YQ3Z', 'Z433DO0IXTSTW8IM', 'stage', '9166644111', 'Fire Emergency', 'Fire!	Emergency' )

	print('SMS has been sent')



while True:
	time.sleep(1)
