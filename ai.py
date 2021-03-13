#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar  9 12:27:15 2021

@author: kuba
"""
import copy
import numpy as np



w = {"H0": {"H0":0.2,"H1": 0.2, "P0": 0.5, "P1": 0.1},
     "H1": {"H0":0.2,"H1": 0.2, "P0": 0.1, "P1": 0.5},
     "P0": {"H0":0.3,"H1": 0.3, "P0": 0.2, "P1": 0.2},
     "P1": {"H0":0.3,"H1": 0.3, "P0": 0.2, "P1": 0.2}
         }


class BeliefSpace:
  def __init__(self, state):
      self.states = []
      
      
    
      
      return self.states
    

class State:
    def __init__(self,player,cards1,cards2,table,deck, parent):
        self.parent = parent
        self.depth = 0
        self.value = 0
      
        self.player = player #player that has the turn, either 1 or 2 (int)
      
        self.cards1 = cards1 #list of cards in player one's hand (Card list) 2cards that need to be created with the Card object
     
        self.cards2 = cards2  #list of cards in AI 's hand (Card list) 2cards that need to be created with the Card object
      
        self.table = table #list of card numbers in the table (int list) 
        #/!\initial table should contain a 0 for the Play action to work
        
        self.deck = deck #number of cards left in the deck (int)
        tableCards =[]
        for nb in table:
            tableCards.append(Card(nb))
            
        self.discoveredCards = cards1+cards2+tableCards #list of all the cards that are out of the deck (list)
    
    
class Card:
  def __init__(self,number):
    self.number = number
    self.known = False
    
  
class Actions:
    def Hint(initialstate,side):
        newstate = copy.deepcopy(initialstate) #side is an integer, 0 = left, 1 = right
        newstate.parent = initialstate
        newstate.depth = initialstate.depth+1
        if initialstate.player == 1:
          newstate.cards2[side].known=True
          newstate.player = 2
        elif initialstate.player == 2:
          newstate.cards1[side].known=True
          newstate.player = 1
        return [newstate]
    
    def Play(initialstate,side): #side is an integer, 0 = left, 1 = right
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
            return newstates
    
class Solver:
    def __init__(self,max_depth):
        self.max_depth = max_depth
        
    def utility(self, state):
        return 10 * len(state.table)
    """
    def forward(self, beliefspace, actions):
        visited = []
        queue = []
        terminal_nodes = []
        for state in beliefspace:
          visited.append(state)
          queue.append(state)
          
        while queue:
          s = queue.pop(0) 
          if s.depth < self.max_depth:
            for action in actions:
                for side in [0, 1]:
                  children = action(s, side)
                  for child in children:
                    queue.append(child)
                    visited.append(child)
                    print(child.depth)
                    if child.depth == self.max_depth:
                    	terminal_nodes.append(child)            
        return terminal_nodes
        """   
    def forward2(self, beliefspace, actions):
        results = []
        for state in beliefspace:
            children = [(self.weighted_value(action(state, side)[0], a_id + str(side)),a_id, side) for (action,a_id) in actions for side in [0, 1]]
            print(children)
            results.append(sorted(children, key=lambda tup: tup[0])[-1])
        
        return results
    
    def max_value(self, state):
        global w
        if state.depth >= self.max_depth:
            return self.utility(state)
        v = - np.inf
        for (a,a_id) in actions:
            for s in range(2):
                v = np.amax(v,self.weighted_value(a(state,s)[0],a_id + str(s)))
        return v
        
        
    def weighted_value(self, state, act_id):
        global w
        weights = w[act_id]
        if state.depth >= self.max_depth:
            return self.utility(state)
        v = 0
        for (a,a_id) in actions:
            for s in range(2):
                v = v + weights[a_id+str(s)]*self.max_value(a(state,s)[0])
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
    actions = [(Actions.Play, "P"), (Actions.Hint, "H")]
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
    
    
    
    
    
    
    