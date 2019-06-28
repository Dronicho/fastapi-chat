from twilio.rest import Client


accound_sid = 'AC026b27e0fd6f4c4c8a55ef6099a21c12'
auth_token = '27915755da99d7a9fed02031274f44da'
client = Client(accound_sid, auth_token)

message = client.messages.create(
    body='test from Andrey:)',
    from_='+12054303935',
    to='+79523187815'
)

print(message.sid)



