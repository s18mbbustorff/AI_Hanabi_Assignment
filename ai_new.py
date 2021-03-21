#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar  9 12:27:15 2021

@author: kuba
"""
import copy
import numpy as np
from BeliefSpace import BeliefSpace

    

class State():
    def __init__(self, Player1, Player2, deck, playedPile, discardPile, hintTokens, penaltyTokens, turn, parent):
        self.Player = Player1
        self.AI = Player2
        self.deck = deck
        self.playedPile = playedPile
        self.discardPile = discardPile
        self.hintTokens = hintTokens
        self.penaltyTokens = penaltyTokens
        self.turn = turn
        
        self.parent = parent
        self.depth = 0
        self.value = 0
        
    def switchTurn(self):
        self.turn = self.turn%2 + 1
        
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
                    
        newState.switchTurn()
        
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
        
        if newState.turn == 1:
            activePlayer = newState.Player
        elif newState.turn == 2:
            activePlayer = newState.AI
        penaltyTokens = newState.penaltyTokens
        deck = newState.deck
        
        playedCard = activePlayer.cards[cardPosition]
        
        #check if the card was correct somehow
        #use functions from the playPile
        verif = newState.playedPile.addCard(playedCard)
        
        if verif == False:
            newState.penaltyTokens.addT()
            newState.discardPile.addCard(playedCard)
        else:
            # instead of drawing we remove a card
            activePlayer.cards.pop(cardPosition)
            
        #activePlayer.draw(deck, cardPosition)
        
        newState.switchTurn()
            
        return newState



class Solver:
    def __init__(self,max_depth, hand_size):
        self.max_depth = max_depth
        self.hand_size = hand_size
        
        self.actions = [[Hint_fun("color"), Hint_fun("number")], Play_fun()]
        
    def utility(self, state):
        utility = 0
        for pile in state.playedPile.piles:
            #print(len(pile))
            utility = utility + len(pile)
            #print(state.penaltyTokens.numberOfTokens)
        return utility * 10 - state.penaltyTokens.numberOfTokens
   
    
    def evaluate(self, beliefspace):
        results =0
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
            results = results + np.array(children)
            actions = [(self.actions[0][0].__dict__, color) for color in np.unique([card.color for card in state.Player.cards])]
            actions = actions + [(self.actions[0][1].__dict__, number) for number in np.unique([card.number for card in state.Player.cards]) ]
            actions = actions + [(self.actions[1].__dict__,pos) for pos in np.arange(len(state.AI.cards))]
            top_action = actions[np.argmax(results)]
        
        return results, actions, top_action
    
    def max_value(self, state):
        global w
        if state is None:
            return - 10
        #print(len(state.Player.cards))
        #print("depth max: ", state.depth)
        if state.penaltyTokens.numberOfTokens != 0:
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
        return v
        
        
    def weighted_value(self, state):
        global w
        if state is None:
            return - 10
        #print("depth weighted: ", state.depth)
        if state.penaltyTokens.numberOfTokens != 0:
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
    
    
    
    
    
    