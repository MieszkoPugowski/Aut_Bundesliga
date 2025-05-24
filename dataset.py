import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin


url = "https://www.football-data.co.uk/austria.php"

def get_bundesliga_results():
    """
    webscraping and downloading a xlsx file with Austrian Bundesliga results from
    https://www.football-data.co.uk/
    """
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')

    # Looping through all links on a site and picking only these with a xlsx file
    # Two links give AUT.xlsx, so we're picking the first one's text
    file_link = [link for link in soup.find_all('a') if link['href'].endswith('xlsx')][0]['href']
    full_url = urljoin(url,file_link)
    file_download = requests.get(full_url)
    with open("AUT.xlsx", "wb") as f:
        f.write(file_download.content)