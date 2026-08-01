import resend
import os
from dotenv import load_dotenv

load_dotenv()
resend.api_key = os.getenv("RESEND_API_KEY")

intro_html = """
<h2>Welcome to LeadPulse!</h2>

<p>You're now set up to receive daily lead digests. Here's a quick guide to reading your emails:</p>

<h3>What is LeadPulse?</h3>
<p>LeadPulse scans Reddit and Hacker News every day for posts where people are asking about 
products like yours. When someone posts "looking for an order tracking tool" or "what do you 
use to manage orders?", LeadPulse catches it and sends it to you so you can respond while the 
conversation is still active.</p>

<h3>How to read your daily digest:</h3>

<p><strong>Score</strong> = A relevance number from 1-20. Higher, more likely to be a real lead. 
Posts where someone is actively looking for a product (Score 10+) are your best opportunities. 
Lower scores (3-5) are general mentions worth scanning but less urgent.</p>

<p><strong>Categories</strong> = Why LeadPulse flagged this post:</p>
<ul>
<li><strong>looking_for</strong> = Someone is actively searching for a product like yours. 
These are your hottest leads. Respond quickly.</li>
<li><strong>pain_point</strong> = Someone is frustrated with their current solution. 
They might be open to switching.</li>
<li><strong>product</strong> = A general mention of your product category. 
Worth reading but less urgent.</li>
</ul>

<p><strong>Source</strong> = Where the post was found (Reddit or Hacker News).</p>

<p><strong>HN Score</strong> = How many upvotes the post has. Higher, more people reading it, more visibility for your response. Reddit posts show 0 because RSS feeds don't include vote counts.</p>

<p><strong>Article Link</strong> = The original article or URL the poster shared.</p>

<p><strong>Discussion</strong> = The Reddit thread or Hacker News comment page. 
<strong>This is where you want to go.</strong> Click this, read the conversation, 
and respond with a genuine, helpful answer mentioning your product.</p>

<h3>Tips for responding:</h3>
<ul>
<li>Be genuine, answer the person's question first, mention your product second</li>
<li>Respond within 24 hours, early responses get the most visibility</li>
<li>Don't copy-paste the same reply everywhere, people notice and it hurts your brand</li>
</ul>

<p>You'll receive your first digest within 24 hours.</p>
<p>If you have any questions, email me at shehanperera1999@gmail.com</p>


<p>Ravidu, LeadPulse</p>
"""

# Send to User 1
resend.Emails.send({
    "from": "onboarding@resend.dev",
    "to": "shehanperera1999@gmail.com",
    "subject": "Welcome to LeadPulse — How to Read Your Daily Digest",
    "html": intro_html
})
print("Intro email sent to User 1!")




