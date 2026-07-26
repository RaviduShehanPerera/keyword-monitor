import requests 

keywords = {"looking_for": ["looking for", "recommend","suggestion","alternative to"],
            "product": ["saas", "startup","tool","platform","software"],
            "pain_point": ["frustrated","struggling","problem with"]}

def calculated_score(story, matched_categories):
    score = 0

    #weight by category
    if "looking_for" in matched_categories:
        score += 10
    if "pain_point" in matched_categories:
        score += 7
    if "product" in matched_categories:
        score += 3

    #weight by HN score (popularity)

    hn_score = story.get("score",0)    
    if hn_score >100:
       score += 5
    elif hn_score >50:
        score +=3
    elif hn_score >10:
        score +=1 

    return score 

#fetch stories 
response = requests.get("https://hacker-news.firebaseio.com/v0/newstories.json")      
story_ids = response.json()[:50]

#for each story check all keyword categories 
matches =[]
for story_id in story_ids:
    response = requests.get (f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json")
    story = response.json()

    if story is None or "title" not in story:
        continue 

    title = story.get("title","").lower()
    text = story.get("text","").lower()
    content = title + " " + text 

    matched_categories =[]
    for category, words in keywords.items():
     for word in words:
        if word in content:
            matched_categories.append(category) 
            break 

    #calculate score
    if matched_categories:
        relevance_score = calculated_score(story, matched_categories)
        matches.append((story, relevance_score, matched_categories))

#sort matches by score(highest first)
matches.sort(key=lambda x:x[1], reverse=True)

#print the results with score
for story,relevance_score,matched_categories in matches: 
    print (f"[Score : {relevance_score}] {story['title']}")
    print(f"Categories: {','.join(matched_categories)}")
    print(f"HN Score: {story.get('score', 0)}")
    print(f"HN Link: https://news.ycombinator.com/item?id={story['id']}")
    print("---")

import csv
from datetime import datetime 

filename = f"hn_results_{datetime.now().strftime('%Y%m%d_%H%M')}.csv"

with open(filename,"w", newline="") as file:
    writer =csv.writer(file)
    writer.writerow(["relevance_score","title","url","hn_score","categories","hn_link","scan_date"])
    for story, relevance_score, matched_categories in matches:
        writer.writerow([
            relevance_score,
            story.get("title",""),
            story.get("url","No Url"),
            story.get("score",0),
            ",".join(matched_categories),
            f"https://news.ycombinator.com/item?id={story['id']}",
            datetime.now().strftime("%Y-%m-%d %H:%M")
        ])
print(f"\nResults saved to {filename}")

