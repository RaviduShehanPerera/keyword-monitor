import requests 

story_id = 49034292
url = f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json"
response = requests.get(url)
story = response.json()
print(story)