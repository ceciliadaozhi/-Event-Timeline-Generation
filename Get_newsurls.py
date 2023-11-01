import requests
from bs4 import BeautifulSoup

from Get_details import get_details

all_news_links = []
base_url = "https://www.bjnews.com.cn/diyikandian/"

# Get 1-51 pages' urls
urls = [base_url + f"{i}.html" for i in range(1, 51)]

for url in urls:
# test code: for url in urls[:2]:
    try:
        payload = {}
        headers = {}
        response = requests.request("GET", url, headers=headers, data=payload)
        print("url:", url)
        print("Response status code:", response.status_code)
        
        soup = BeautifulSoup(response.text, 'html.parser')
        pin_demo_divs = soup.find_all('div', class_='pin_demo')

        for div in pin_demo_divs:
            link_element = div.find('a')
            link_href = link_element['href'] if link_element else None
            if link_href:
                all_news_links.append(link_href)
    
    except requests.RequestException as e:
        print(f"Error fetching URL {url}: {e}")

for link in all_news_links:
# test code: for link in all_news_links[:3]:
    details = get_details(link)
    if details:
        print("Title:", details['title'])
        print("Publish Time:", details['publish_time'])
        print("Source:", details['source'])
        print("-----")


