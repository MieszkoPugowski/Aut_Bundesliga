import random
from elo_ratings import LeagueElo
from random_fixture import CreateFixture
from collections import defaultdict
import pandas as pd

class MonteCarloSim:
    def __init__(self,country:str,n:int=1):
        self.n = n
        self.league_dict = {}
        self.country_name = country
        self.elo = LeagueElo(country=self.country_name)
        self.season_dict = CreateFixture(country=self.country_name).create_gameweeks_dict()

    def simulate_one_game(self,home,away):
        assert home,away in self.elo.ratings.keys()
        result_probs = {"home":0,"draw":0,"away":0}
        rand = random.random()
        probs = self.elo.match_result_probabilities(home,away)
        if rand < probs["home_win"]:
            result_probs["home"] += 1
        elif rand <probs["home_win"]+probs["draw"]:
            result_probs["draw"] += 1
        else:
            result_probs["away"] += 1
        return result_probs

    def simulate_season_xp(self):
        def calculate_xpts(PW, PD):
            xP = (3 * PW) + PD
            return xP

        position_counts = defaultdict(lambda: defaultdict(int))
        xPts_totals = defaultdict(float)
        elo = LeagueElo(self.country_name)

        for i in range(0, self.n):
            league_dict = defaultdict(int)
            for gameweek in self.season_dict:
                for game in self.season_dict[gameweek]:
                    result = self.simulate_one_game(game[0], game[1])
                    exp_win = elo.match_result_probabilities(game[0], game[1])["home_win"]
                    exp_draw = elo.match_result_probabilities(game[0], game[1])["draw"]
                    exp_away = elo.match_result_probabilities(game[0], game[1])["away_win"]

                    if result["home"]:
                        elo.update_elo_ratings(game[0], game[1], 1, exp_win)
                    elif result["away"]:
                        elo.update_elo_ratings(game[0], game[1], 0, exp_win)
                    else:
                        elo.update_elo_ratings(game[0], game[1], 0.5, exp_win)

                    home_xPts = calculate_xpts(exp_win, exp_draw)
                    away_xPts = calculate_xpts(exp_away, exp_draw)

                    league_dict[game[0]] += home_xPts
                    league_dict[game[1]] += away_xPts
                    xPts_totals[game[0]] += home_xPts
                    xPts_totals[game[1]] += away_xPts

            standings = sorted(league_dict.items(), key=lambda x: x[1], reverse=True)
            for position, (team, _) in enumerate(standings, 1):
                position_counts[team][position] += 1

        pos_df = pd.DataFrame().from_dict(position_counts, orient="index")
        pos_df = pos_df.reindex(sorted(pos_df.columns), axis=1)
        pos_df = pos_df.sort_values(
            by=list(pos_df.columns),
            ascending=[False] * len(pos_df.columns),
            kind='mergesort'
        ).fillna(0).mul(1 / self.n).round(2)

        avg_xPts = {team: total / self.n for team, total in xPts_totals.items()}
        xPts_df = pd.DataFrame.from_dict(avg_xPts, orient='index', columns=['Avg_xPts'])
        xPts_df = xPts_df.sort_values('Avg_xPts', ascending=False).round(2)

        return pos_df.merge(xPts_df,left_index=True,right_index=True).sort_values("Avg_xPts",ascending=False)