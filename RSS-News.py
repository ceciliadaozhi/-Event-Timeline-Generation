import requests
from bs4 import BeautifulSoup

all_news_links = []
base_url = "http://feeds.bbci.co.uk/news/rss.xml"

urls = [base_url]

for url in urls:
    try:
        payload = {}
        headers = {}
        response = requests.request("GET", url, headers=headers, data=payload)
        # print("url:", url)
        print("Response status code:", response.status_code)
        # print("Response text:", response.text)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find all <item> elements
        items = soup.find_all('item')
        
        # Extract 'title', 'link', and 'pubdate' from each item
        news_items = []
        for item in items:
            title = item.find('title').text
            link = item.find('guid').text
            pub_date = item.find('pubdate').text
            
            news_items.append({
                'title': title,
                'link': link,
                'pubDate': pub_date
            })
        
        # Now 'news_items' contains all the extracted information
        # for news_item in news_items:
            # print(news_item)

        # save to bbc_news.csv
        import csv
        with open('bbc_news1.csv', 'w', newline='') as csvfile:
            fieldnames = ['title', 'link', 'pubDate']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for news_item in news_items:
                writer.writerow(news_item)
    
    except requests.RequestException as e:
        print(f"Error fetching URL {url}: {e}")
        continue