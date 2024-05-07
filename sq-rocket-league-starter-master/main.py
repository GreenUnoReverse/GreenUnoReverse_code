#3 TODO: don't run into the interior wall in the goal
#665 TODO: during kickoff: get boost on the way to ball

from util.objects import *
from util.routines import *
from util.tools import find_hits

class Bot(GoslingAgent):
    def run(self):
        if self.get_intent() is not None:
            return
        
# KICKOFF #

        if self.kickoff_flag: 
            self.set_intent(kickoff()) 
            return  

# VARIABLES #

        targets = {
            'at_opponent_goal': (self.foe_goal.left_post, self.foe_goal.right_post),
            'away_from_our_net': (self.friend_goal.right_post, self.friend_goal.left_post)
        }

        d1 = abs(self.ball.location.y - self.foe_goal.location.y) # distance from ball to goal
        d2 = abs(self.me.location.y - self.foe_goal.location.y) + 300 # distance from me to goal
        is_in_front_of_ball = d1 > d2
        # middle_available_boosts = [boost for boost in self.boosts if boost.large and boost.active and boost.index >= 15 and boost.index <= 18]
        orange_available_boosts = [boost for boost in self.boosts if boost.large and boost.active and boost.index > 28]
        blue_available_boosts = [boost for boost in self.boosts if boost.large and boost.active and boost.index < 5]

        hits = find_hits(self,targets)

        if self.friend_goal.location.y > 0: # > 0 prints orange; < 0 prints blue
            team = 1 # orange (cringe)
            colour = "orange"
        elif self.friend_goal.location.y < 0:
            team = -1 # blue
            colour = "blue"

# DE FENCE #           

        if team * self.ball.location.y > 0: # ball is on our side
            print(colour, ": AHHHHHHHHHHHHHHHHHHHHHH!!")
            if len(hits['at_opponent_goal']) > 0:
                print(colour + ': AH! at their goal')
                self.set_intent(hits['at_opponent_goal'][0])
                return
            elif len(hits['away_from_our_net']) > 0:
                print(colour + ': AH! away from our goal')
                self.set_intent(hits['away_from_our_net'][0])
                return
            else: 
                self.set_intent(goto(self.friend_goal.location))
        else: # ball is on opponent's side
            width = 200
            for thingy in range(len(self.boosts)): # thingy is boost
                if self.boosts[thingy].location.x < self.me.location.x + width and self.boosts[thingy].location.x > self.me.location.x - width and self.boosts[thingy].location.y > self.me.location.y and self.boosts[thingy].location.y < self.ball.location.y: # if boost is between car and ball
                    self.set_intent(goto(thingy))
                    return

# A FENCE #

            if len(hits['at_opponent_goal']) > 0: 
                self.set_intent(hits['at_opponent_goal'][0])
                print(colour + ': at their goal')
                return

# RETREAT #

        if is_in_front_of_ball:
            if self.me.boost < 30:
                if team == 1:
                    defense_available_boosts = orange_available_boosts
                else:
                    defense_available_boosts = blue_available_boosts
                if len(defense_available_boosts) > 0:
                    while self.me.boost < 30:
                        self.set_intent(goto(defense_available_boosts[0].location))
                        print(colour + ": going for boost", defense_available_boosts[0].index)
                        return
                return 
            else:
                self.set_intent(goto(self.friend_goal.location))
            return

        if len(hits['away_from_our_net']) > 0:
            print(colour + ': away from our goal')
            self.set_intent(hits['away_from_our_net'][0])
            return
        
        # if ball x_pos * team > 0, ball is on our side
        #    hit the ball toward opponent's side
        # else ball x_pos * team < 0, ball is on opponent's side

        # if self.ball.location.x