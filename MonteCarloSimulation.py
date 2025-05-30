import random
from elo_ratings import BundesligaElo
from random_fixture import CreateFixture
from typing import Dict
import time
from collections import defaultdict
import pandas as pd

season_dict = CreateFixture().create_gameweeks_dict()
elo = BundesligaElo()

league_dict = {}
for team in elo.ratings.keys():
    league_dict[team] = 0
start_time = time.time()
class MonteCarloSim:
    def __init__(self,n:int=1):
        self.n = n

    def simulate_one_game(self,home,away):
        assert home,away in elo.ratings.keys()
        result_probs = {"home":0,"draw":0,"away":0}
        rand = random.random()
        probs = elo.match_result_probabilities(home,away)
        if rand < probs["home_win"]:
            result_probs["home"] += 1
        elif rand <probs["home_win"]+probs["draw"]:
            result_probs["draw"] += 1
        else:
            result_probs["away"] += 1
        return result_probs

    def simulate_season(self, season_fixture:Dict=season_dict):
        position_counts = defaultdict(lambda: defaultdict(int))
        elo = BundesligaElo()
        for i in range(0,self.n):
            # Reset league points and elo ratings for each simulation
            # Reset league points for each simulation
            league_dict = defaultdict(int)
            for gameweek in season_fixture:
                for game in season_fixture[gameweek]:
                    result = self.simulate_one_game(game[0],game[1])
                    exp_win = elo.match_result_probabilities(game[0],game[1])["home_win"]
                    if result["home"]:
                        league_dict[game[0]] += 3
                        elo.update_elo_ratings(game[0], game[1], 1, exp_win)
                    elif result["away"]:
                        league_dict[game[1]] += 3
                        elo.update_elo_ratings(game[0], game[1], 0, exp_win)
                    else:
                        league_dict[game[0]] += 1
                        league_dict[game[1]] += 1
                        elo.update_elo_ratings(game[0], game[1], 0.5, exp_win)
            standings = sorted(league_dict.items(),key=lambda x:x[1],reverse=True)
            for position, (team, _) in enumerate(standings, 1):
                position_counts[team][position] += 1
        df = pd.DataFrame().from_dict(position_counts,orient="index")
        df = df.reindex(sorted(df.columns), axis=1)
        # Sort by most 1st places, then 2nd places, etc.
        df = df.sort_values(
            by=list(df.columns),
            ascending=[False] * len(df.columns),
            kind='mergesort'
        ).fillna(0).mul(1/self.n).round(2)
        return df
end_time = time.time()
print(f"The simulation took: {round(end_time-start_time,5)}s")