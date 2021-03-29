#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar  9 12:27:15 2021

@author: kuba
"""
import copy
import numpy as np
from BeliefSpace import BeliefSpace

    

class State_search:
    def __init__(self, Player1, Player2, deck, playedPile, discardPile, hintTokens, penaltyTokens, turn, parent):
        self.Player = Player1
        self.AI = Player2
        self.deck = deck
        self.playedPile = playedPile
        self.discardPile = discardPile
        self.hintTokens = hintTokens
        self.penaltyTokens = penaltyTokens
        self.turn = turn
        
        if turn == 1:
            self.human = True
        else:
            self.human = False
        self.parent = parent
        self.depth = 0
        self.value = 0
        
    def switchTurn(self):
        self.turn = self.turn%2 + 1
        self.human = not self.human
    
    #def __eq__(self, other):
    #print(self.__dict__)
    #return self.__dict__ == other.__dict__
    
    
class Card():
    
    #-----------------------------
    #-----Initialization functions
    #-----------------------------
    
    def __init__(self,color,number):
        self.color = color
        self.number = number
        self.colorHinted = False
        self.numberHinted = False
        
    def sayInfo(self):
        print ("Color: {}, number: {}.".format(self.color,self.number))
    def storeInfo(self):
        return "Color: {}, number: {}.".format(self.color,self.number)
        
    def __eq__(self, other):
       
        return self.__dict__ == other.__dict__
    
  
class Hint_fun:
    def __init__(self,h_type):
        self.h_type = h_type
        self.name = "hint"
    def __call__(self, initialState, hint = None):
        #hintType: String. Can be "number" or "color"
        #hint: String ("red","green",...) or Int ("1","2","3","4" or "5")
        
        #initializing variables (extracted from state)
        newState = copy.deepcopy(initialState)
        newState.parent = initialState
        newState.depth = initialState.depth+1
        human = False #newState.human
        
        if newState.turn == 1:
            activePlayer = newState.Player
            otherPlayer = newState.AI
        elif newState.turn == 2:
            activePlayer = newState.AI
            otherPlayer = newState.Player
        hintTokens = newState.hintTokens
        
        #print("hint:", hint)
        if hintTokens == 0:
            #print ("Error. Number of Hint Tokens is 0. You cannot make a Hint.")
            return None
        
        if otherPlayer.allHintsGiven(hint, self.h_type):
                #print ("Error. Hint already given or no cards correspond to the hint. You cannot make that hint.")
                return None
        if hint != None:    
            for i in range(len(otherPlayer.cards)):
                if self.h_type == "color":
                    if otherPlayer.cards[i].color == hint:
                        otherPlayer.cards[i].colorHinted = True
                elif self.h_type == "number":
                    if otherPlayer.cards[i].number == hint:
                        otherPlayer.cards[i].numberHinted = True
        hintTokens.removeT(human)
        newState.turn = newState.turn%2 + 1            
        #newState.switchTurn()
        
        return newState

    
class Play_fun: 
    def __init__(self):
        self.name = "play"
    def __call__(self,initialState, cardPosition): #side is an integer, 0 = left, 1 = right
        #cardPosition: Int. Index of the card you want to play from your hand.
        
        #initializing variables (extracted from state)
        newState = copy.deepcopy(initialState)
        newState.parent = initialState
        newState.depth = initialState.depth+1
        human = False
        
        if newState.turn == 1:
            activePlayer = newState.Player
        elif newState.turn == 2:
            activePlayer = newState.AI
        penaltyTokens = newState.penaltyTokens
        deck = newState.deck
        
        playedCard = activePlayer.cards[cardPosition]
        
        #check if the card was correct somehow
        #use functions from the playPile
        verif = newState.playedPile.addCard(playedCard, human)
        
        if verif == False:
            newState.penaltyTokens.addT(human)
            newState.discardPile.addCard(playedCard)
        else:
            # instead of drawing we remove a card
            activePlayer.cards.pop(cardPosition)
            
        #activePlayer.draw(deck, cardPosition)
        newState.turn = newState.turn%2 + 1  
        #newState.switchTurn()
            
        return newState

class Discard_fun:
        #cardPosition: Int. Index of the card you want to discard from your hand.
        def __init__(self):
             self.name = "discard"
        def __call__(self,initialState, cardPosition):
            #initializing variables (extracted from state)
            newState = copy.deepcopy(initialState)
            newState.parent = initialState
            newState.depth = initialState.depth+1
            human = False #newState.human
            
            if newState.turn == 1:
                activePlayer = newState.Player
            elif newState.turn == 2:
                activePlayer = newState.AI
            hintTokens = newState.hintTokens
            deck = newState.deck
            
            if (hintTokens.numberOfTokens == hintTokens.maxTokens):
                #print ("Error. Number of Hint Tokens is maxed. You cannot discard a card.")
                return None
            
            discardedCard = activePlayer.cards[cardPosition]
            newState.discardPile.addCard(discardedCard)
            #activePlayer.draw(deck, cardPosition)
            hintTokens.addT(human)
            
            newState.turn = newState.turn%2 + 1  
            #newState.switchTurn()
            
            return newState
    


class Solver:
    def __init__(self,max_depth, hand_size):
        self.max_depth = max_depth
        self.hand_size = hand_size
        
        self.actions = [[Hint_fun("color"), Hint_fun("number")], Play_fun(), Discard_fun()]
        
    def utility(self, state):
        utility = 0
        for pile in state.playedPile.piles:
            #print(len(pile))
            utility = utility + len(pile)
            #print(state.penaltyTokens.numberOfTokens)
        return utility * 10 - 5*state.penaltyTokens.numberOfTokens - len(state.discardPile.cards)
   
    
    def evaluate(self, beliefspace, test):
        results = 0
        for state in beliefspace:
            # TO DO
            # IF AN ACTION IS NOT PERMISIBLE RETURN NONE (action that would lose a life is not permisible)
            # PLAY RETURNS ONLY ONE STATE AND IT DELETES THE PLAYED CARDS FROM THE PLAYERS HANDS
            # CHECK FOR IDENTICAL STATES
            # HINT FUNCTION SHOULD BE ABLE NOT TO GIVE HINT (Player giving a hint to the AI)
            #print(np.unique([card.color for card in state.Player.cards]))
            """
            children = [(self.weighted_value(self.actions[0][0](state,color)) ,self.actions[0][0].__dict__, color) for color in np.unique([card.color for card in state.Player.cards]) ] # giving hint color
            children = children + [(self.weighted_value(self.actions[0][1](state, number)),self.actions[0][1].__dict__, number) for number in np.unique([card.number for card in state.Player.cards]) ] # giving hint color
            children = children + [(self.weighted_value(self.actions[1](state, pos)),self.actions[1].__dict__,pos) for pos in np.arange(len(state.AI.cards))] # playing card
            #print(children)
            #results.append(sorted(children, key=lambda tup: tup[0]))
            """
            children = [self.weighted_value(self.actions[0][0](state,color)) for color in np.unique([card.color for card in state.Player.cards]) ] # giving hint color
            children = children + [self.weighted_value(self.actions[0][1](state, number)) for number in np.unique([card.number for card in state.Player.cards]) ] # giving hint color
            children = children + [self.weighted_value(self.actions[1](state, pos)) for pos in np.arange(len(state.AI.cards))] # playing card
            children = children + [self.weighted_value(self.actions[2](state, pos)) for pos in np.arange(len(state.AI.cards))] # discarding a card
            results = results + np.array(children)
            actions = [(self.actions[0][0].__dict__, color) for color in np.unique([card.color for card in state.Player.cards])]
            actions = actions + [(self.actions[0][1].__dict__, number) for number in np.unique([card.number for card in state.Player.cards]) ]
            actions = actions + [(self.actions[1].__dict__,pos) for pos in np.arange(len(state.AI.cards))]
            actions = actions + [(self.actions[2].__dict__,pos) for pos in np.arange(len(state.AI.cards))]
            
            
        sorted_list = sorted([(action,-value) for action, value in zip(actions, results)], key=lambda element: (element[1], element[0][0]["name"],str(element[0][1])))
        #top_action = actions[np.argmax(results)]
        top_action = sorted_list[0][0] 
        #print(sorted_list)
        
        if test:
            #print(sorted_list)
            return results, actions, top_action
        else:
            if top_action[0]["name"] == "play":
                print("The computer played: ", state.AI.cards[top_action[1]].storeInfo())
                return 1,top_action[1]
            elif top_action[0]["name"] == "hint":
                print("You got a hint: ", str(top_action[0]["h_type"]) + " " +str(top_action[1]))
                return 2,(top_action[0]["h_type"], top_action[1])
            elif top_action[0]["name"] == "discard":
                print("The computer discarded: ", state.AI.cards[top_action[1]].storeInfo())
                return 3, top_action[1]
        
    
    def max_value(self, state):
        global w
        if state is None:
            return 0
        #print(len(state.Player.cards))
        #print("depth max: ", state.depth)
        initialPenaltyTokens = state.parent.penaltyTokens.numberOfTokens
        finalPenaltyTokens = state.penaltyTokens.numberOfTokens
        difPenaltytokens = finalPenaltyTokens - initialPenaltyTokens
        
        if difPenaltytokens != 0:
            return -10
        if state.depth >= self.max_depth:
            return self.utility(state)
        v = - np.inf
        # giving hints colors
        for card in state.Player.cards:
            v = max(v,self.weighted_value(self.actions[0][0](state,card.color)))
        # giving hints numbers
            v = max(v,self.weighted_value(self.actions[0][1](state,card.number)))
        
        # playing cards 
        for pos in np.arange(len(state.AI.cards)):
            v = max(v,self.weighted_value(self.actions[1](state, pos)))
            v = max(v,self.weighted_value(self.actions[2](state, pos)))
            
        return v
        
        
    def weighted_value(self, state):
        global w
        if state is None:
            #print("BOOM")
            return - 10
        #print("depth weighted: ", state.depth)
        initialPenaltyTokens = state.parent.penaltyTokens.numberOfTokens
        finalPenaltyTokens = state.penaltyTokens.numberOfTokens
        difPenaltytokens = finalPenaltyTokens - initialPenaltyTokens
        
        if difPenaltytokens != 0:
            return -10
        # Calculate probabilities for what might the player play, if there is a hint on a card, playing this card is more probable than other actions
        # If there are no hints, giving a hint is the most probable
        # However if a player gives us a hint, it has no new information for us -> idle state
        if state.depth >= self.max_depth:
            return self.utility(state)
        """
        a = np.ones(len(state.Player.cards))
        for i in range(len(a)):
            if state.Player.cards[i].colorHinted or state.Player.cards[i].numberHinted:
                a[i] = 2
            if state.Player.cards[i].colorHinted and state.Player.cards[i].numberHinted:
                a[i] = 4
        if a.sum() == len(state.Player.cards): # if there are no hints on the cards
            w_hint = 2/(2 + len(state.Player.cards))
            w_play = 1/(2 + len(state.Player.cards))
        else: #if there are hints on the cards
            w_hint = 1/(a.sum())
            w_play = 1/(a.sum())
        """
        a = np.zeros(len(state.Player.cards))
        for i in range(len(a)):
            if state.Player.cards[i].colorHinted or state.Player.cards[i].numberHinted:
                a[i] = 1
            if state.Player.cards[i].colorHinted and state.Player.cards[i].numberHinted:
                a[i] = 2
        if a.sum() == 0: # if there are no hints on the cards
            w_hint = 1
            w_play = 0
        else: #if there are hints on the cards
            w_hint = 1/(a.sum())/3
            w_play = 2/(a.sum())/3
        v = w_hint*self.max_value(self.actions[0][0](state))
        
        for pos in np.arange(len(state.Player.cards)):
            v = v + w_play*a[pos]*self.max_value(self.actions[1](state, pos))
        return v
  
  
#if __name__ == "__main__":
    
    #c1 = Card(1)
    #c2 =  Card(2)
    #c3 =  Card(3)
    #c4 =  Card(4)
    #c5 =  Card(5)
    #cards1 = [c5, c1]
    #cards2 = [c2, c4]
    #table = [0]
    #deck = 1
    #parent = None
    #player = 2
    #state = State(player,cards1,cards2,table,deck, parent)
    #initial_belief_states = [state]
    #solver = Solver(2, 4)
    #states = firstTest()
    #state = states[0]
    #terminal = solver.evaluate([state])
    
    
    
    """
    print("Some tests to see the Actions funtioning:")
    print("0.Initial state with cards: player1: (1,2), player2: (3,4)")
    state1 = State(1,[Card(1),Card(2)],[Card(4),Card(5)],[0],1,None)
    print("")
    print("1.Making a Hint of the 2nd player right card:")
    state2 = Actions.Hint(state1,1)
    #check that the card is now "known" and that the player becomes "2"
    print("Is the card known? {}. What player turn is it after the action? {}.".format(state2[0].cards2[1].known,state2[0].player))
    print("")
    print("2. Playing the correct card from player 1's left (the 1):")
    state2b = Actions.Play(state1,0)
    print("New size of deck: {}. New card on the left for player 1: {}. New table: {}. Amount of new states created: {}".format(state2b[0].deck,state2b[0].cards1[0].number,state2b[0].table,len(state2b)))
    print(state2[0].depth)
    state3 = Actions.Hint(state2[0],1)
    print(state3[0].depth)
    state4 = Actions.Hint(state3[0],1)
    print(state4[0].depth)
    """
    """
    [[(0.0, {'h_type': 'color', 'name': 'hint'}, 'blue'),
   (-6.666666666666666, {'h_type': 'color', 'name': 'hint'}, 'red'),
   (6.666666666666666, {'h_type': 'number', 'name': 'hint'}, 1),
   (-6.666666666666666, {'h_type': 'number', 'name': 'hint'}, 3),
   (-6.666666666666666, {'h_type': 'number', 'name': 'hint'}, 4),
   (-10, {'name': 'play'}, 0),
   (10.0, {'name': 'play'}, 1),
   (-10, {'name': 'play'}, 2),
   (-10, {'name': 'play'}, 3)]],
   """
    
    
    
    
    
    