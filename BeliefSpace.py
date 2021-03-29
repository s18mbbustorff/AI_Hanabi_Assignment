#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 16 11:53:02 2021
@author: kuba
"""


from tests import firstTest
from HanabiClasses import Card
import copy
from itertools import combinations


class BeliefSpace:
  def __init__(self, state, hand_size):
      self.states = []
      state.depth = 0
      deck =  state.deck.storeInfo()
      deck = [(i,j) for [i,j] in deck]
      #state.penaltyTokens.numberOfTokens = 0
      
      
      #Reduce the belief space if the AI cards have hints
      hinted = []
      not_hinted_indeces = []
      for i in range(len(state.AI.cards)):
          if state.AI.cards[i].colorHinted or state.AI.cards[i].numberHinted:
              hinted.append((state.AI.cards[i].number,state.AI.cards[i].color))
          else:
              not_hinted_indeces.append(i)
      
      
      
      player2 = [(i,j) for [i,j] in state.AI.storeInfo() if (i,j) not in hinted]
      unknown = player2 + deck
      
      #print(player2)
      comb = set(list(combinations(unknown,hand_size - len(hinted))))
      #print(len(comb))
      #print(comb)
      for i in comb:
          newstate = copy.deepcopy(state)
          deck = [item for item in unknown if item not in i]
          newstate.deck = [Card(k[1], k[0]) for k in deck]
          
          new = [Card(k[1], k[0]) for k in i]
          for ind, k in enumerate(not_hinted_indeces):
              newstate.AI.cards[k] = new[ind]
              
          self.states.append(newstate)
    



if __name__ == "__main__":
    states = firstTest()
    state1 = states[0]
    state1.AI.cards[2].colorHinted = True
    space = BeliefSpace(state1,4)
    #for state in space.states:
        #print(state.Player2.storeInfo())
        
    #print(state1.Player1.storeInfo())   
    #print(state.Player1.storeInfo())   