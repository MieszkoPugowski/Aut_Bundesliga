import random

class CreateFixture:
    def __init__(self):
        self.teams = [
        "Wolfsberger AC", "Austria Vienna", "SK Rapid", "Sturm Graz",
        "BW Linz", "Salzburg", "Hartberg", "Tirol", "Grazer AK", "LASK",
        "Altach", "Ried"
    ]
        self.fixtures=[]


    def _generate_fixtures(self,teams):
        n = len(teams)
        rounds = []

        for round_num in range(n - 1):
            pairings = []
            for i in range(n // 2):
                home = self.teams[i]
                away = self.teams[n - 1 - i]
                if round_num % 2 == 0:
                    pairings.append((home, away))
                else:
                    pairings.append((away, home))
            rounds.append(pairings)
            self.teams.insert(1, self.teams.pop())  # Rotate

        return rounds
    def _set_fixtures_order(self):
        random.shuffle(self.teams)
        first_half = self._generate_fixtures(self.teams[:])
        second_half = [[(away, home) for (home, away) in round] for round in first_half]
        self.all_rounds = first_half + second_half

    def create_gameweeks_list(self):
        self._set_fixtures_order()
        games_dict = {}
        for gw, matches in enumerate(self.all_rounds, start=1):
            match_list = []
            for match in matches:
                lineup=(match[0],match[1])
                match_list.append(lineup)
            games_dict[gw]=match_list
        self.fixtures.append(games_dict)
        return self.fixtures