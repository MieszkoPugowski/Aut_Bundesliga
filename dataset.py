import io
import pandas as pd
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

class GetBundesligaResults:
    """
    webscraping and downloading a xlsx file with Austrian Bundesliga results from
    https://www.football-data.co.uk/
    """
    def __init__(self):
        self.url ="https://www.football-data.co.uk/austria.php"
        self.df = None

    def _get_bundesliga_results(self):
        r = requests.get(self.url)
        soup = BeautifulSoup(r.content, 'html.parser')

        # Looping through all links on a site and picking only these with a xlsx file
        # Two links give AUT.xlsx, so we're picking the first one's text
        file_link = [link for link in soup.find_all('a') if link['href'].endswith('csv')][0]['href']
        full_url = urljoin(self.url,file_link)
        file_download = requests.get(full_url)
        self.file_content = file_download.content.decode('utf-8')


    def _clean_dataframe(self) -> pd.DataFrame:
        df = pd.read_csv(io.StringIO(self.file_content))
        df = df.drop(columns=['Country','League','MaxCH','MaxCD','MaxCA',
                       'BFECH','BFECD','BFECA','PSCD','PSCH','PSCA'])
        df = df.rename(columns={"HG":"Home_goals","AG":"Away_goals","Res":"Result"})
        return df

    def return_df(self):
        self._get_bundesliga_results()
        return self._clean_dataframe()

