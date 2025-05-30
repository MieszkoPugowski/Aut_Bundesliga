import pandas as pd
import penaltyblog as pb
from dataset import GetBundesligaResults
from random_fixture import CreateFixture

training_data = GetBundesligaResults().return_df()
training_data["Date"] = pd.to_datetime(training_data["Date"],dayfirst=True)

# create and train Bivariate Poisson model with added weights for recent games

weights = pb.models.dixon_coles_weights(training_data["Date"], 0.001)
clf = pb.models.BivariatePoissonGoalModel(training_data["Home_goals"],
                                          training_data['Away_goals'],
                                          training_data['Home'],
                                          training_data['Away'],
                                          weights)
clf.fit()

def calculate_xPts(PW,PD):
    xP =(3*PW)+PD
    return xP

# importing a random fixture list
gameweek_dict = CreateFixture().create_gameweeks_dict()
table = []

#creating a Bundesliga table in form of list of dictionaries
for team in gameweek_dict.teams:
    points = {"name":team,"xP":0,"xGD":0}
    table.append(points)

def model_the_league():
    '''
    Function that calculates table based on expected Points (xP) after one randomized
    gameweek
    :return:
    '''
    for i in range(1,23):
        for game in gameweek_dict[i]:
            result = clf.predict(game[0],game[1])
            H_xP = calculate_xPts(result.home_win,result.draw)
            next(filter(lambda x:x["name"]==game[0],table))["xP"]+=float(H_xP)

            H_xGD = result.home_goal_expectation-result.away_goal_expectation
            next(filter(lambda x:x["name"]==game[0],table))["xGD"]+=float(H_xGD[0])

            A_xP = calculate_xPts(result.away_win,result.draw)
            next(filter(lambda x:x["name"]==game[1],table))["xP"]+=float(A_xP)

            A_xGD = -H_xGD
            next(filter(lambda x:x["name"]==game[1],table))["xGD"]+=float(A_xGD[0])

    return pd.DataFrame(table).sort_values("xP",ascending=False).reset_index(drop=True)