import io
import pandas as pd
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

class Fbref:
    def __init__(self,season:str="2025-2026",league:str="Austrian-Bundesliga"):
        self.season = season
        self.league = league

    def fixtures(self):
        # try:
        #TODO - make it accessible for other leagues, the issue lies with 'comps/56' line
        #TODO - as it redirects to Austrian Bundesliga directly, you gotta think here
        df = pd.read_html(f"https://fbref.com/en/comps/56/{self.season}/schedule/{self.season}-{self.league}-Scores-and-Fixtures",
                          attrs = {'id':"sched_2025-2026_56_1"})[0]
        fixtures = df.iloc[:,[0,4,6]]
        fixt_dict = (
        fixtures.groupby('Wk')[['Home', 'Away']]
        .apply(lambda x: list(map(tuple, x.values)))
        .to_dict()
        )
        return fixt_dict