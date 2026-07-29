import resend 
import os
from dotenv import load_dotenv

load_dotenv()

resend.api_key = os.getenv("RESEND_API_KEY")

email = resend.Emails.send ({
    "from": "onboarding@resend.dev",
    "to":"shehanperera1999@gmail.com",
    "subject":"LeadPulse Test Email",
    "html":"<h1>It works!</h1><p>Your LeadPulse email system is connected.</p>"

})

print(email)