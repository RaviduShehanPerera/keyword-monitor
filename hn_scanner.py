import requests 

keywords = ["ai", "python", "open source", "startup", "google", "api"]


#get the lastest story Ids 
response = requests.get("https://hacker-news.firebaseio.com/v0/newstories.json")
story_ids = response.json()[:50]

#check the story for key words 
matches=[]
for story_id in story_ids:
    url = f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json"
    response = requests.get(url)
    story = response.json()

    #some stories might be missing a title 
    if story is None or "title" not in story:
        continue

    title = story["title"].lower()

    for keyword in keywords:
        if keyword in title:
            matches.append(story)
            break

#print the results 

print(f"\nfound {len(matches)} matching stories:\n")
for story in matches:
    print(f"title: {story['title']}")
    print(f"URL: {story.get('url','No Url')}")
    print(f"score; {story.get('score',0)}")
    print(f"HN Link: https://news.ycombinator.com/item?id={story['id']}")
    print("---")