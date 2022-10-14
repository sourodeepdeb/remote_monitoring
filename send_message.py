# Download the helper library from https://www.twilio.com/docs/python/install
import os
from twilio.rest import Client


# Your Account Sid and Auth Token from twilio.com/console
# and set the environment variables. See http://twil.io/secure
account_sid = "AC4e6bd38a02ec20478fa1caf668434116"
auth_token = "3fa734f4d8164ae9d1a4c98ccddfc3af"
client = Client(account_sid, auth_token)

message = client.messages \
    .create(
         body='New Raspberry Pi - Testing message sending',
         from_='+15102567788',
         to='+19082793566'
     )

print(message.sid)
