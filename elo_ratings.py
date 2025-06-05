import requests
from datetime import date
from urllib.parse import urljoin
import pandas as pd
import io
import numpy as np
import math

class LeagueElo:
    def __init__(self,country:str,k:float = 20.0,home_advantage:float =29.6):
        self.hfa = home_advantage
        self.k = k
        self.country_name = country
        self.ratings = self.get_todays_league_elo()

    def _get_todays_elo(self):
        # think about getting hfa from here and changing self.hfa
        # think about picking only teams from the top league
        url = "http://api.clubelo.com/"
        today_date = str(date.today())
        file_download = urljoin(url,today_date)
        response = requests.get(file_download)
        file_content = response.content.decode('utf-8')
        today_elo_csv = pd.read_csv(io.StringIO(file_content))
        return today_elo_csv

    def get_todays_league_elo(self):
        today_elo = self._get_todays_elo()
        league_today = (today_elo[(today_elo["Country"] == self.country_name) & (today_elo["Level"] == 1)]
        .reset_index(drop=True)[["Club", "Elo"]]).to_dict()
        league_dict = {}
        for club in league_today["Club"]:
            key = league_today["Club"][club]
            value = league_today["Elo"][club]
            league_dict[key]=value
        return league_dict

    def match_result_probabilities(self,home,away):
        assert home,away in self.ratings.keys()
        elo_home = self.ratings[home]+self.hfa
        elo_away = self.ratings[away]
        elo_diff = elo_home-elo_away

        p_draw = float(1/math.sqrt(2*np.pi*np.e) * np.exp(-((elo_diff/200)**2)/(2*(np.e**2))))
        p_home = float(1 / (1 + 10 ** (-elo_diff / 400)))-(0.5*p_draw)
        p_away = float(1 / (1 + 10 ** (elo_diff / 400)))-(0.5*p_draw)
        return {"home_win": p_home, "draw": p_draw, "away_win": p_away}

    def update_elo_ratings(self,home,away,result,exp_result,k:float = 20.0):
        self.ratings[home] = self.ratings[home]+k*(result-exp_result)
        self.ratings[away] = self.ratings[away]-k*(result-exp_result)