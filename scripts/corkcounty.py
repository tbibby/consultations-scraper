import requests
from bs4 import BeautifulSoup
from datetime import datetime
from extract_dates import analyse_text_for_earliest_and_last_date
from tipp import description_escaped_html
import html

# URL of the website
domain = 'https://www.corkcoco.ie'
urls38 = 'https://www.corkcoco.ie/en/resident/planning-and-development/public-consultations/current-section-38s'
urlp8 = 'https://www.corkcoco.ie/en/resident/planning-and-development/public-consultations/active-part-8-development-consultation'
author = 'Cork County Council'
#i have to use absolute paths on the server
rss_path = '../rss/corkcounty.rss.xml'
# rss_path = '/home/tbibbyie/projects.bibby.ie/consultations-scraper/rss/corkcounty.rss.xml'

# Send a GET request
responses38 = requests.get(urls38)
soup38 = BeautifulSoup(responses38.content, 'html.parser')
responsep8 = requests.get(urlp8)
soup8 = BeautifulSoup(responsep8.content, 'html.parser')
items = []
rows38 = soup38.select('.main-content article')
for row in rows38:
    title_element = row.select_one('h3 a')
    if title_element is not None:
        #print(title_element)
        item = {
            'title': title_element.get_text(),
            'link': domain + title_element['href'],
            'pubDate': datetime.now().strftime('%a, %d %b %Y %H:%M:%S %z'),
        }
        items.append(item)

rows8 = soup8.select('.main-content article')
for row in rows8:
    title_element = row.select_one('h3 a')
    if title_element is not None:
        item = {
            'title': title_element.get_text(),
            'link': domain + title_element['href'],
            'pubDate': datetime.now().strftime('%a, %d %b %Y %H:%M:%S %z'),
        }
        items.append(item)
full_items = []
#ok now we've got lots of items, let's loop through them, visit the link, try and extract some stuff
for item in items:
    response= requests.get(item['link'])
    soup = BeautifulSoup(response.content, 'html.parser')
    content = soup.select_one('.field__item')
    if content is not None:
        # extract item date, closing date, title, description
        content_text = content.get_text()
        #extract dates
        (earliest, latest) = analyse_text_for_earliest_and_last_date(content_text)
        description_html = description_escaped_html("Open", earliest, latest, item['title'], content)
        fixed_title = item['title'].replace('&','&amp;')
        full_item = {
            'title': fixed_title,
            'link': item['link'],
            'pubDate': earliest,
            'description': description_html
        }
        unescaped_html = html.unescape(description_html)
        #print(unescaped_html)
        #print("-------------")
        full_items.append(full_item)

    else:
        # idk I guess skip it and print an error?
        print(f"**********DID NOT GET A HIT FOR {item['link']}*********")


# Function to create RSS feed
def create_rss_feed(items):
    rss_items = ""
    for item in items:
        guid = item['link']
        description = item['description']
        rss_items += f"""
        <item>
            <title>{item['title']}</title>
            <link>{item['link']}</link>
            <pubDate>{item['pubDate']}</pubDate>
            <author>{author}</author>
            <guid isPermaLink="true">{guid}</guid>
            <description>{description}</description>
        </item>
        """

    rss_feed = f"""<?xml version="1.0" encoding="UTF-8" ?>
    <rss version="2.0">
        <channel>
            <title>Cork County Council Open Consultations (Part 8 and Section 38)</title>
            <link>{urls38}</link>
            <description>List of open Section 38 and Part 8 consultations</description>
            {rss_items}
        </channel>
    </rss>"""

    return rss_feed

# Generate RSS feed
rss_feed = create_rss_feed(full_items)

# Save to a file
with open(rss_path, 'w+') as file:
    file.write(rss_feed)
