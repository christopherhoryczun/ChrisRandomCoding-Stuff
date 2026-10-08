#pip install twilio

from twilio.rest import Client

# 1. Paste your Twilio credentials here
ACCOUNT_SID = "your_account_sid_here"
AUTH_TOKEN = "your_auth_token_here"

# 2. Initialize the Twilio Client
client = Client(ACCOUNT_SID, AUTH_TOKEN)

# 3. Define the message details
# Note: Phone numbers must use the E.164 format (e.g., +15558675309)
message = client.messages.create(
    body="Hello from VS Code and Python! 🐍🚀",
    from_="+1XXXXXXXXXX",  # Your Twilio phone number
    to="+1YYYYYYYYYY"      # Your personal phone number
)

# 4. Print confirmation to the terminal
print(f"✅ Text message sent successfully! Message SID: {message.sid}")

#Running Code
#python TextMe.py


#For more Notes and information go to TextMe.md
