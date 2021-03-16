#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar  9 12:27:15 2021

@author: kuba
"""
import copy
import numpy as np


class BeliefSpace:
  def __init__(self, state):
      self.states = []
      
      return self.states
    

class State():
    def __init__(self, Player1, Player2, deck, playedPile, discardPile, hintTokens, penaltyTokens, turn, parent):
        self.Player1 = Player1
        self.Player2 = Player2
        self.deck = deck
        self.playedPile = playedPile
        self.discardPile = discardPile
        self.hintTokens = hintTokens
        self.penaltyTokens = penaltyTokens
        self.turn = turn
        
        self.parent = parent
        self.depth = 0
        self.value = 0
        
        
    def __eq__(self, other):
       
        return self.__dict__ == other.__dict__
    
    
class Card():
    
    #-----------------------------
    #-----Initialization functions
    #-----------------------------
    
    def __init__(self,color,number):
        self.color = color
        self.number = number
        self.colorHinted = False
        self.numberHinted = False
        
    def __eq__(self, other):
       
        return self.__dict__ == other.__dict__
    
  
class Hint_fun:
    def __init__(self,h_type):
        self.h_type = h_type
        self.name = "hint"
    def __call__(self,initialstate,side = None):
        newstate = copy.deepcopy(initialstate) #side is an integer, 0 = left, 1 = right
        newstate.parent = initialstate
        newstate.depth = initialstate.depth+1
        if side != None:
            newstate.hands[initialstate.player - 1][side].known=True
        newstate.player = 3 - initialstate.player
    
        return [newstate]

    
class Play_fun: 
    def __init__(self):
        self.name = "play"
    def __call__(self,initialstate,side): #side is an integer, 0 = left, 1 = right
        newstate = copy.deepcopy(initialstate)
        newstate.parent = initialstate
        newstate.depth = initialstate.depth+1
        #------------------------
        #if no cards left in deck
        if initialstate.deck == 0:
            if initialstate.player == 1:
                playedcard = initialstate.cards1[side]
                if playedcard.number == (max(initialstate.table)+1): #check if it is a correct card
                    newstate.table.append(playedcard.number) #it is added to the table of the new state
                newstate.cards1[side] = None #remove card from hand
                newstate.player = 2 #change player turn
            
            elif initialstate.player == 2:
                playedcard = initialstate.cards2[side]
                if playedcard.number == (max(initialstate.table)+1): #if it is a correct card
                    newstate.table.append(playedcard.number) #it is added to the table of the new state
                newstate.cards2[side] = None
                newstate.player = 1
            
            return [newstate]
        #----------------------------
        #if there are cards left in the deck, we need to make a new state for each possibility of a new card
        #the function will return a list of new states
        else: 
            #initializing the list of newstates
            nbCardsLeft = initialstate.deck
            newstates = [None] * nbCardsLeft
            for i in range(nbCardsLeft):
                newstates[i] = copy.deepcopy(newstate)
        
        	#making a list of all the possible numbers left
            discoveredNumbers = []
            for card in initialstate.discoveredCards:
                discoveredNumbers.append(card.number)
            allNumbers = [1,2,3,4,5]
            numbersLeft = [x for x in allNumbers if x not in discoveredNumbers]
            #updating all the new states with all possible new cards
            #then removing the played card (add its number to table if correct)
            if initialstate.player == 1:
                playedcard = initialstate.cards1[side]
                for i in range(nbCardsLeft):
                    newstates[i].cards1[side] = Card(numbersLeft[i]) #old card that was played gets replaced by new card
                    if playedcard.number == (max(initialstate.table)+1): #if it is a correct card
                        newstates[i].table.append(playedcard.number) #it is added to the table of the new state
                    
                    newstates[i].player = 2
            elif initialstate.player == 2:
                playedcard = initialstate.cards2[side]
                for i in range(nbCardsLeft):
                    newstates[i].cards2[side] = Card(numbersLeft[i]) #old card that was played gets replaced by new card
                    if playedcard.number == (max(initialstate.table)+1): #if it is a correct card
                        newstate.table.append(playedcard.number) #its number is added to the table of the new state
                
                    newstates[i].player = 1
                    
            for state in newstates:
                state.deck = initialstate.deck-1
            return newstates[0] # should return only one state



class Solver:
    def __init__(self,max_depth, hand_size):
        self.max_depth = max_depth
        self.hand_size = hand_size
        
        self.actions = [[Hint_fun("color"), Hint_fun("number")], Play_fun()]
        
    def utility(self, state):
        return 10 * len(state.table)
   
    
    def evaluate(self, beliefspace):
        results = []
        for state in beliefspace:
            # TO DO
            # IF AN ACTION IS NOT PERMISIBLE RETURN NONE (action that would lose a life is not permisible)
            # PLAY RETURNS ONLY ONE STATE AND IT DELETES THE PLAYED CARDS FROM THE PLAYERS HANDS
            # CHECK FOR IDENTICAL STATES
            # HINT FUNCTION SHOULD BE ABLE NOT TO GIVE HINT (Player giving a hint to the AI)
            children = [(self.weighted_value(action(state, pos),action.__dict__),action.__dict__,pos) for action in self.actions[0] for pos in np.arange(len(state.hands[2 - state.player]))] # giving hint
            children = children + [(self.weighted_value(self.actions[1](state, pos),self.actions[1].__dict__,pos),self.actions[1].__dict__,pos) for pos in np.arange(len(state.hands[state.player]))] # playing card
            print(children)
            results.append(sorted(children, key=lambda tup: tup[0])[-1])
        
        return results
    
    def max_value(self, state):
        global w
        if state == None:
            return 0
        if state.depth >= self.max_depth:
            return self.utility(state)
        v = - np.inf
        # giving hints
        for action in self.actions[0]: 
            for pos in np.arange(len(state.hands[2 - state.player])):
                v = np.amax(v,self.weighted_value(action(state,pos)))
        # playing cards 
        for pos in np.arange(len(state.hands[state.player])):
            v = np.amax(v,self.weighted_value(self.actions[1](state, pos)))
        return v
        
        
    def weighted_value(self, state):
        global w
        if state == None:
            return 0
        # Calculate probabilities for what might the player play, if there is a hint on a card, playing this card is more probable than other actions
        # If there are no hints, giving a hint is the most probable
        # However if a player gives us a hint, it has no new information for us -> idle state
        if state.depth >= self.max_depth:
            return self.utility(state)
        a = np.ones(len(state.hands[state.player]))
        for i in range(len(state.hands[state.player])):
            if state.hands[state.player][i].colorHinted or state.hands[state.player][i].numberHinted:
                a[i] = 2
            if state.hands[state.player][i].colorHinted and state.hands[state.player][i].numberHinted:
                a[i] = 4
        if a.sum() == len(state.hands[state.player]): # if there are no hints on the cards
            w_hint = 2/(2 + len(state.hands[state.player]))
            w_play = 1/(2 + len(state.hands[state.player]))
        else: #if there are hints on the cards
            w_hint = 1/(a.sum())
            w_play = 1/(a.sum())
            
        v = w_hint*self.max_value(self.actions[0][0](state))
        for pos in np.arange(len(state.hands[state.player])):
            v = v + w_play*a[pos]*self.max_value(self.actions[1](state, pos))
        return v
  
  
if __name__ == "__main__":
    
    c1 = Card(1)
    c2 =  Card(2)
    c3 =  Card(3)
    c4 =  Card(4)
    c5 =  Card(5)
    cards1 = [c5, c1]
    cards2 = [c2, c4]
    table = [0]
    deck = 1
    parent = None
    player = 2
    state = State(player,cards1,cards2,table,deck, parent)
    initial_belief_states = [state]
    solver = Solver(2)
    terminal = solver.forward2(initial_belief_states, actions)
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
    
    
    
    
    
    
    