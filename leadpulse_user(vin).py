import requests 
import csv
import resend 
import os
import feedparser
from datetime import datetime
from dotenv import load_dotenv
from urllib.parse import quote
import time 

load_dotenv()
resend.api_key = os.getenv("RESEND_API_KEY")

#---KEYWORDS---
keywords = {
    "looking_for": ["looking for", "recommend", "suggestion", "alternative to",
                     "what do you use", "anyone know", "best way to"],
    "product": ["cat toy", "cat toys", "interactive cat toy", "automatic cat toy",
                "dog toy", "dog toys", "indestructible dog toy", "chew toy",
                "pet toy", "pet toys", "durable dog toy", "smart cat toy"],
    "pain_point": ["frustrated", "bored cat", "destructive dog",
                   "breaks everything", "chewed through", "destroyed",
                   "keeps breaking", "nothing lasts"]
}

#---SCORING---
def calculated_score(story, matched_categories):
    score = 0
    
    # High score only when intent + product match together
    if "looking_for" in matched_categories and "product" in matched_categories:
        score += 15
    elif "looking_for" in matched_categories:
        score += 3
    
    if "pain_point" in matched_categories and "product" in matched_categories:
        score += 12
    elif "pain_point" in matched_categories:
        score += 3
    
    if "product" in matched_categories:
        score += 3
    
    hn_score = story.get("score", 0)
    if hn_score > 100:
        score += 5
    elif hn_score > 50:
        score += 3
    elif hn_score > 10:
        score += 1
    
    return score

#---BUILD EMAIL---
def build_email_html(matches):
    if not matches:
        return"<h2>LeadPulse Daily Digest</h2><p>No matches found today.</p>"
    
    html= "<h2>Leadpulse Daily Digest</h2>"
    html+=f"<p>Found {len(matches)} leads - {datetime.now().strftime('%B %d, %Y')}</p>"
    html +="<hr>"

    for story,relevance_score,matched_categories in matches:
        title =story.get("title","No title")
        url =story.get("url","")
        if str(story['id']).startswith("http"):
            hn_link=story['id']
        else:
            hn_link = f"https://news.ycombinator.com/item?id={story['id']}"
            
        hn_score = story.get("score",0)
        categories =",".join(matched_categories)

        html += f"<div style ='margin-bottom: 20px;'>"
        html += f"<h3>[Score: {relevance_score}] {title}</h3>"
        html += f"<p><strong>Categories:</strong> {categories}</p>"
        html +=f"<p><strong>HN Score:</strong> {hn_score}</p>"
        html += f"<p><strong>Source:</strong> {story.get('source', 'Unknown')}</p>"
        if url:
            html +=f"<p><a href='{url}'>Article Link</a> | <a href='{hn_link}'>Discussion</a></p>"
        else:
            html += f"<p><a href='{hn_link}'>View Discussion</a></p>"
        html +=f"</div><hr>" 
    return html     

#---SCAN HACKER NEWS---
print('Scanning Hacker News...')
response = requests.get("https://hacker-news.firebaseio.com/v0/newstories.json")
story_ids = response.json()[:200]

matches =[]
seen_titles = set()
for story_id in story_ids:
    response = requests.get(f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json")
    story = response.json()    

    if story is None or "title" not in story:
        continue                    
    title =story.get("title","").lower()
    text = story.get("text","").lower()
    content = title + " " + text

    matched_categories =[]
    for category,words in keywords.items():
        for word in words:
            if word in content:
                matched_categories.append(category)
                break

    if matched_categories:
        if story.get ("title","").lower() not in seen_titles:
            seen_titles.add(story.get("title","").lower())
            story["source"]="Hacker News"
            relevance_score = calculated_score(story,matched_categories)
            matches.append((story,relevance_score,matched_categories))

print(f"found {len(matches)} HN matches")

#---SCAN SUBREDDIT---
subreddits = ["cats", "dogs", "pets", "CatAdvice", "DogAdvice",
              "petcare", "BuyCatStuff", "DogCare"]

print("Scanning subreddit...")
for subreddit in subreddits:
    
    feed = feedparser.parse(f"https://www.reddit.com/r/{subreddit}/new.rss")
    print(f"  r/{subreddit}: {len(feed.entries)} posts")
    for entry in feed.entries[:3]:
        print(f"    - {entry.title}")

    for entry in feed.entries:
        title= entry.title.lower()

        matched_categories =[]
        for category,words in keywords.items():
            for word in words:
                if word in title:
                    matched_categories.append(category)
                    break

        if matched_categories:
            if entry.title.lower() not in seen_titles:
                seen_titles.add(entry.title.lower())
                story={
                    "title":entry.title,
                    "url":entry.link,
                    "id":entry.link,
                    "score":0,
                    "source":"Reddit"
                }
                relevance_score = calculated_score(story,matched_categories)
                matches.append((story,relevance_score,matched_categories))
"""
#---SEARCH ALL OF REDDIT---
search_terms = ["order tracking", "order management", "whatsapp orders",
                "delivery tracking", "shipment tracking", "track orders",
                "order management tool", "manage orders whatsapp",
                "order tracking app", "shipping management",
                "inventory tracking", "fulfillment software","whatsapp seller orders", "order chaos",
                "manage orders", "order system small business"]

print("Searching Reddit...")
for term in search_terms:
    search_url = f"https://www.reddit.com/search.rss?q={quote(term)}&sort=new&t=month"
    headers = {"User-Agent": "LeadPulse/1.0 by Ravidu"}
    response = requests.get(search_url, headers=headers)
    print(f"  '{term}': status {response.status_code}")
    feed = feedparser.parse(response.text)
    print(f"  '{term}': {len(feed.entries)} results")
    time.sleep(10)

    for entry in feed.entries:
        title = entry.title.lower()
        
        matched_categories = []
        for category, words in keywords.items():
            for word in words:
                if word in title:
                    matched_categories.append(category)
                    break
        
        if entry.title.lower() not in seen_titles:
            seen_titles.add(entry.title.lower())
            story = {
                "title": entry.title,
                "url": entry.link,
                "id": entry.link,
                "score": 0,
                "source": "Reddit Search"
            }
            relevance_score = calculated_score(story, matched_categories)
            matches.append((story, relevance_score, matched_categories))
"""
# --- SCAN PRODUCT HUNT ---
print("Scanning Product Hunt...")
ph_feed = feedparser.parse("https://www.producthunt.com/feed")

for entry in ph_feed.entries:
    title = entry.title.lower()
    
    matched_categories = []
    for category, words in keywords.items():
        for word in words:
            if word in title:
                matched_categories.append(category)
                break
    
    if matched_categories:
        if "product" not in matched_categories:
            matched_categories.append("product")
        if entry.title.lower() not in seen_titles:
            seen_titles.add(entry.title.lower())
            story = {
                "title": entry.title,
                "url": entry.link,
                "id": entry.link,
                "score": 0,
                "source": "Product Hunt"
            }
            relevance_score = calculated_score(story, matched_categories)
            matches.append((story, relevance_score, matched_categories))
"""
# --- SCAN DEV.TO ---
print("Scanning Dev.to...")
for term in ["order tracking", "order management", "ecommerce tools"]:
    devto_feed = feedparser.parse(f"https://dev.to/feed/tag/{quote(term)}")
    
    for entry in devto_feed.entries:
        title = entry.title.lower()
        
        matched_categories = []
        for category, words in keywords.items():
            for word in words:
                if word in title:
                    matched_categories.append(category)
                    break
        
        if matched_categories:
            if "product" not in matched_categories:
                matched_categories.append("product")
            if entry.title.lower() not in seen_titles:
                seen_titles.add(entry.title.lower())
                story = {
                    "title": entry.title,
                    "url": entry.link,
                    "id": entry.link,
                    "score": 0,
                    "source": "Dev.to"
                }
                relevance_score = calculated_score(story, matched_categories)
                matches.append((story, relevance_score, matched_categories))
"""
matches.sort(key=lambda x:x[1], reverse=True)
print(f"Total matches : {len(matches)}") 
#matches = [(story,score,cats)for story,score,cats in matches if score>=6]
#print(f"Quality leads: {len(matches)}")

#---SEND EMAIL---
if not matches:
    print("No quality leads found today. Skipping email and csv file")
else:    
    email_html = build_email_html(matches)
    
    email = resend.Emails.send({
        "from": "onboarding@resend.dev",
        "to": "shehanperera1999@gmail.com",
        "subject": f"LeadPulse Digest - {datetime.now().strftime('%B %d, %Y')}",
        "html": email_html
    })
    print(f"Email sent! ID: {email}")
"""
#---SAVE TO CSV---
    filename = f"hn_results_{datetime.now().strftime('%Y%m%d_%H%M')}.csv"
    with open(filename,"w",newline="")as file:
        writer =csv.writer(file)
        writer.writerow(["relevance_score","title","url","hn_score","categories","hn_link","scan_date"])
        for story,relevance_score,matched_categories in matches:
            writer.writerow([
                relevance_score,
                story.get("title",""),
                story.get("url","No URL"),
                story.get("score",0),
                ",".join(matched_categories),
                f"https://news.ycombinator.com/item?id={story['id']}",
                datetime.now().strftime("%Y-%m-%d %H:%M")
        ])
    print(f"Results saved to {filename}")        
"""    