import pandas as pd
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import pandas


class GetBundesligaResults:
    """
    webscraping and downloading a xlsx file with Austrian Bundesliga results from
    https://www.football-data.co.uk/
    """
    def __init__(self):
        self.url ="https://www.football-data.co.uk/austria.php"
        self._get_bundesliga_results()
        self._clean_dataframe()

    def _get_bundesliga_results(self):
        r = requests.get(self.url)
        soup = BeautifulSoup(r.content, 'html.parser')

        # Looping through all links on a site and picking only these with a xlsx file
        # Two links give AUT.xlsx, so we're picking the first one's text
        file_link = [link for link in soup.find_all('a') if link['href'].endswith('xlsx')][0]['href']
        full_url = urljoin(self.url,file_link)
        file_download = requests.get(full_url)
        with open("AUT.xlsx", "wb") as f:
            f.write(file_download.content)

    def _clean_dataframe(self):
        clean_df = pd.read_excel("AUT.xlsx")
        clean_df = clean_df.drop(columns=['Country','League','MaxCH','MaxCD','MaxCA',
                       'BFECH','BFECD','BFECA'])
        clean_df = clean_df.rename(columns={"HG":"Home_goals","AG":"Away_goals","Res":"Result"})
        clean_df.to_csv("AUT.csv")