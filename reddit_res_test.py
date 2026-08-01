import requests 
url = "https://www.reddit.com/r/startups/new.rss"
headers = {"User-Agent": "LeadPulse/1.0 by Ravidu"}
response = requests.get(url, headers=headers)

print(response.status_code)
print(response.text[:10000])