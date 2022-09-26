import random
random.seed(31337)

NUM_COOPERATOR = 0

NUM_DEFECTOR = 0
NUM_TITFORTAT = 0
NUM_GRIMTRIGGER = 0
NUM_COINFLIPPER = 0
NUM_DIEROLLER = 0

POINTS_BOTH_COOPERATE = 1
POINTS_BOTH_DEFECT = 0
POINTS_BETRAYER = 2
POINTS_BETRAYED = -1

GAMES_PER_MATCH = 200

def main():
    the_dilemma = Dilemma(POINTS_BOTH_COOPERATE,POINTS_BOTH_DEFECT,POINTS_BETRAYER,POINTS_BETRAYED)

    prisoners = []
    for i in range(NUM_COOPERATOR):
        prisoners.append(Cooperator())
    for i in range(NUM_DEFECTOR):
        prisoners.append(Defector())
    for i in range(NUM_TITFORTAT):
        prisoners.append(TitForTat())
    for i in range(NUM_GRIMTRIGGER):
        prisoners.append(GrimTrigger())
    for i in range(NUM_COINFLIPPER):
        prisoners.append(Coinflipper())
    for i in range(NUM_DIEROLLER):
        prisoners.append(Dieroller())
    for i in range(len(prisoners)):
        for j in range(i+1,len(prisoners)):
            the_dilemma.play(prisoners[i],prisoners[j],GAMES_PER_MATCH)
    print("\n****RESULTS****")
    for prisoner in sorted(prisoners,reverse=True):
        print(prisoner)

#Prisoner class
class _Prisioner():
    def __init__(self):
        self.points = 0
    def update(self,was_betrayed,earned_points):
        self.earned_points = earned_points
        self.points += self.earned_points
    def match_reset(self):
        pass
    def get_name(self):
        return self.name
    def get_points(self):
        return self.points
    def __lt__(self,other):
        return self.points < other.points
    def __ge__(self,other):
        return self.points >= other.points
    def __str__(self):
        return f"{self.get_name()}: {self.points} points"
        
#Cooperator class
class Cooperator(_Prisioner):
    num_cooperator = 1
    def __init__(self):
        super().__init__()
        self.name = f"Cooperator {Cooperator.num_cooperator}"
        Cooperator.num_cooperator += 1
    def play(self):
        return False
 
#Defector class
class Defector(_Prisioner):
    num_defector = 1
    def __init__(self):
        super().__init__()
        self.name = f"Defector {Defector.num_defector}"
        Defector.num_defector += 1
    def play(self):
        return True

#TitForTat class
class TitForTat (_Prisioner):
    num_T4T = 1
    def __init__(self):
        super().__init__()
        self.name = f"GrimTrigger {GrimTrigger.num_grimtrigger}"
        TitForTat.num_T4T += 1
    def match_reset(self):
        self.got_betrayed = False
        
    def update(self,was_betrayed,earned_points):
        super().update(was_betrayed,earned_points)
        self.was_betrayed = was_betrayed
        if self.was_betrayed== True:
            self.got_betrayed = True
        else:
            self.got_betrayed = False
      
    def play(self):
        if self.got_betrayed:
            return True
        return False
    
#GrimTrigger class
class GrimTrigger(_Prisioner):
    num_grimtrigger = 1
    
    def __init__(self):
        super().__init__()
        self.name = f"GrimTrigger {GrimTrigger.num_grimtrigger}"
        GrimTrigger.num_grimtrigger += 1
        
    def match_reset(self):
        self.got_betrayed = False
        
    def update(self,was_betrayed,earned_points):
        super().update(was_betrayed,earned_points)
        self.was_betrayed = was_betrayed
        if self.was_betrayed== True:
            self.got_betrayed = True
    
    def play(self):
        if self.got_betrayed == True:
            return True
        return False
    
#CoinFlipper class
class Coinflipper(_Prisioner):
    num_coinflipper = 1
    
    def __init__(self):
        super().__init__()
        self.name = f"Coin Flipper {Coinflipper.num_coinflipper}"
        Coinflipper.num_coinflipper += 1
        
    def play(self):
        x = random.random()
        return(x <= 0.5)
        
#DieRoller class
class Dieroller (_Prisioner):
    num_dieroller = 1
    
    def __init__(self):
        super().__init__()
        self.name = f"Die Roller {Dieroller.num_dieroller}"
        Dieroller.num_dieroller += 1
        
    def play(self):
        x = random.random()
        return(x <= 1/6)     

class Dilemma:

    def __init__(self,both_coop_outcome,both_defect_outcome,betrayer_outcome,betrayed_outcome):
        self.both_coop_outcome = both_coop_outcome
        self.both_defect_outcome = both_defect_outcome
        self.betrayer_outcome = betrayer_outcome
        self.betrayed_outcome = betrayed_outcome

    def play(self,player1,player2,num_games):
        player1.match_reset()
        player2.match_reset()
        player1_starting_score = player1.get_points()
        player2_starting_score = player2.get_points()

        for i in range(num_games):
        
            player1_choice = player1.play()
            player2_choice = player2.play()

            if player1_choice:
                if player2_choice:
                    player1.update(True,self.both_defect_outcome)
                    player2.update(True,self.both_defect_outcome)
                else:
                    player1.update(False,self.betrayer_outcome)
                    player2.update(True,self.betrayed_outcome)
            else:
                if player2_choice:
                    player1.update(True,self.betrayed_outcome)
                    player2.update(False,self.betrayer_outcome)
                else:
                    player1.update(False,self.both_coop_outcome)
                    player2.update(False,self.both_coop_outcome)

        player1_ending_score = player1.get_points()
        player2_ending_score = player2.get_points()
        change_in_player1_score = player1_ending_score-player1_starting_score
        change_in_player2_score = player2_ending_score-player2_starting_score
        print(f"{player1.get_name()} ({change_in_player1_score}) vs. {player2.get_name()} ({change_in_player2_score})")

if __name__ == "__main__":
    main()
    

