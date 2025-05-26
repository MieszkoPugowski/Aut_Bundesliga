import pandas as pd
import penaltyblog as pb
from dataset import GetBundesligaResults



BUNDESLIGA_RESULTS = GetBundesligaResults().return_df()
BUNDESLIGA_TEAMS = ["Wolfsberger AC", "Austria Vienna", "SK Rapid", "Sturm Graz",
                    "BW Linz", "Salzburg", "Hartberg","Tirol","Grazer AK","LASK",
                    "Altach","Ried"]

PI_RATINGS = pb.ratings.PiRatingSystem()



class PiRatingCalculator:
    '''
    Calculating Pi Rating for each Bundesliga team.
    For more info, read: https://pena.lt/y/2025/04/14/pi-ratings-the-smarter-way-to-rank-football-teams/
    '''
    def __init__(self):
        self.teams_list = BUNDESLIGA_TEAMS
        self.teams_ratings = []
        self._update_pi_ratings()

    def _update_pi_ratings(self):
        for idx, row in BUNDESLIGA_RESULTS.iterrows():
            goal_diff = row["Home_goals"] - row["Away_goals"]
            PI_RATINGS.update_ratings(row["Home"], row["Away"], goal_diff, row["Date"])

    def calculate_rating(self):
        for team in self.teams_list:
            team_rating = [x for x in PI_RATINGS.rating_history if x["team"] == team]
            self.teams_ratings.append(team_rating)
        self._create_dataframe()

    def _create_dataframe(self):
        ratings_df = pd.DataFrame()
        for list in self.teams_ratings:
            df = pd.DataFrame(list)
            ratings_df = pd.concat([ratings_df,df])
        ratings_df.to_csv("pi_ratings.csv",index=False)