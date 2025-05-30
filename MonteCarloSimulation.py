import random
from elo_ratings import BundesligaElo
from random_fixture import CreateFixture
from typing import Dict
import time

season_dict = CreateFixture().create_gameweeks_dict()
elo = BundesligaElo()

league_dict = {}
for team in elo.ratings.keys():
    league_dict[team] = 0
start_time = time.time()
class MonteCarloSim:
    def __init__(self,n:int=1):
        self.n = n

    def simulate_one_game(self,home,away,n=1):
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

