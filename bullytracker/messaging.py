from twilio.rest import Client
import json


cred = json.load(open("twiliocred.json", "r"))

twilio_account = cred["twilio_account"]
auth_token = cred["auth_token"]

client = Client(twilio_account, auth_token)


def send_sms_alert(phone_number, student_name, location):
    phone_number = "whatsapp:" + phone_number
    print("Sending message to: " + phone_number)
    message = client.messages.create(
        to=phone_number,
        from_="whatsapp:+13203144053",
        content_sid="HX4836808ff291aa3f60848495fb23b5da",
        content_variables=json.dumps({"1": student_name, "2": location}),
    )
    print(message.sid)
