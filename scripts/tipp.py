import requests
from bs4 import BeautifulSoup
from datetime import datetime

# URL of the website
url = 'https://consultations.tipperarycoco.ie/consultations'
author = 'Tipperary County Council'

# Send a GET request
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

# Use CSS selectors to find elements
rows = soup.select('.open-consultations .views-row')
items = []
for row in rows:
    title_element = row.select_one('.consult-title a')
    date_element = row.select_one('.consult-day time')
    
    if title_element and date_element:
        item = {
            'title': title_element.get_text(),
            'link': url + title_element['href'],
            'pubDate': datetime.fromisoformat(date_element['datetime']).strftime('%a, %d %b %Y %H:%M:%S %z'),
        }
        items.append(item)

# Function to create RSS feed
def create_rss_feed(items):
    rss_items = ""
    for item in items:
        guid = item['link']
        rss_items += f"""
        <item>
            <title>{item['title']}</title>
            <link>{item['link']}</link>
            <pubDate>{item['pubDate']}</pubDate>
            <author>{author}</author>
            <guid isPermaLink="true">{guid}</guid>
        </item>
        """

    rss_feed = f"""<?xml version="1.0" encoding="UTF-8" ?>
    <rss version="2.0">
        <channel>
            <title>Tipperary County Council Open Consultations</title>
            <link>{url}</link>
            <description>List of open consultations</description>
            {rss_items}
        </channel>
    </rss>"""

    return rss_feed

# Generate RSS feed
rss_feed = create_rss_feed(items)

# Save to a file
with open('/home/tbibbyie/projects.bibby.ie/consultations-scraper/rss/tipperary.rss.xml', 'w+') as file:
    file.write(rss_feed)
