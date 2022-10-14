# Download the helper library from https://www.twilio.com/docs/python/install
import os
from twilio.rest import Client


# Your Account Sid and Auth Token from twilio.com/console
# and set the environment variables. See http://twil.io/secure
account_sid = "xxxxxxxx"
auth_token = "xxxxx"
client = Client(account_sid, auth_token)

message = client.messages \
    .create(
         body='New Raspberry Pi - Testing message sending',
         from_='+15102567788',
         to='+19082793566'
     )

print(message.sid)
