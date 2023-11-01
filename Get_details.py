from bs4 import BeautifulSoup
import requests

def get_details(url):
    try:
        payload = {}
        headers = {}
        response = requests.request("GET", url, headers=headers, data=payload)
        
        soup = BeautifulSoup(response.text, 'html.parser')
        # Get the title
        title = soup.find('h1').text
        
        # Get the publish time
        publish_time = soup.find('span', class_='timer').text

        # Get the source
        source = soup.find('em').text

        return {
            'title': title,
            'publish_time': publish_time,
            'source': source
        }

    except requests.RequestException as e:
        print(f"Error fetching URL {url}: {e}")
        return None
