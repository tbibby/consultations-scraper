import requests
from bs4 import BeautifulSoup
from datetime import datetime
import html
from dateutil import parser

def description_escaped_html(status, start_date, closing_date, title, description):
    attr_date_format = '%Y-%m-%dT%H:%M:%S%z'
    desc_date_format = '%-d.%m.%Y - %I:%M%P' #%P is undocumented and, confusingly, lowercase
    start_date_attr = start_date.strftime(attr_date_format)
    start_date_desc = start_date.strftime(desc_date_format)
    closing_date_attr = closing_date.strftime(attr_date_format)
    closing_date_desc = closing_date.strftime(desc_date_format)

    html_description = f"""
    <div class="status">
        <span class="label">Status:</span> 
        <span class="value">{status}</span>
    </div>
    <div class="period">
        <span class="label">Open Period:</span>
        <span class="value">
                <span  class="date-display-range">
                        <span  property="dc:date" datatype="xsd:dateTime" content="{start_date_attr}" class="date-display-start">
                                {start_date_desc}
                        </span>
                        to
                        <span  property="dc:date" datatype="xsd:dateTime" content="{closing_date_attr}" class="date-display-end">
                                {closing_date_desc}
                        </span>
                </span>
        </span>
    </div>
    <div class="summary">
        <p>
                {title}
        </p>
        <p>
                {description}
        </p>
    </div>
    """
    return html.escape(html_description)

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
    closing_element = row.select_one('.consult-closing-date time')
    desc_element = row.select_one('.consult-body')
    #OF COURSE the closing date is in a different format. Python doesn't like the Z
    closing_date = parser.parse(closing_element['datetime'])
    start_date = datetime.fromisoformat(date_element['datetime'])
    title = title_element.get_text()
    #ok to have html in the description
    description = desc_element.select_one('p').find(string=True, recursive=False) #don't get link text in a tag
    if title_element and date_element:
        item = {
            'title': title_element.get_text(),
            'link': url + title_element['href'],
            'pubDate': datetime.fromisoformat(date_element['datetime']).strftime('%a, %d %b %Y %H:%M:%S %z'),
            'description': description_escaped_html(status='Open', start_date=start_date, closing_date=closing_date, title=title_element.get_text(), description=description),
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
            <description>{item['description']}</description>
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
with open('../rss/tipperary.rss.xml', 'w+') as file:
    file.write(rss_feed)
