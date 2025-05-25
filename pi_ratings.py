import pandas as pd
import penaltyblog as pb
from dataset import get_bundesliga_results

# # run only once
# get_bundesliga_results()

BUNDESLIGA_TEAMS = ["Wolfsberger AC", "Austria Vienna", "SK Rapid", "Sturm Graz",
                    "BW Linz", "Salzburg", "Hartberg","Tirol","Grazer AK","LASK",
                    "Altach","A. Klagenfurt"]
PI_RATINGS = pb.ratings.PiRatingSystem()

#reading Excel file and cleaning data
# For the glossary, read: https://www.football-data.co.uk/notes.txt
BUNDESLIGA_RESULTS = pd.read_excel("AUT.xlsx").drop(columns=["BFECH","BFECD","BFECA"])
BUNDESLIGA_RESULTS.rename(columns={"HG":"home_goals","AG":"away_goals","Res":"Result"},inplace=True)


class PiRatingCalculator:
    '''
    Calculating Pi Rating for each Bundesliga team.
    For more info, read: https://pena.lt/y/2025/04/14/pi-ratings-the-smarter-way-to-rank-football-teams/
    '''
    def __init__(self,teams:list,):
        self.teams_list = teams
        self.teams_ratings = []
        self._update_pi_ratings()

    def _update_pi_ratings(self):
        for idx, row in BUNDESLIGA_RESULTS.iterrows():
            goal_diff = row["home_goals"] - row["away_goals"]
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