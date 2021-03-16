#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 16 11:53:02 2021

@author: kuba
"""


from tests import firstTest
from ai_new import Card
import copy
from itertools import combinations


class BeliefSpace:
  def __init__(self, state, hand_size):
      self.states = []
      
      deck =  state.deck.storeInfo()
      deck = [(i,j) for [i,j] in deck]
      player2 = [(i,j) for [i,j] in state.Player2.storeInfo()]
      unknown = player2 + deck
      
      comb = set(list(combinations(unknown,hand_size)))
      print(len(comb))
      for i in comb:
          newstate = copy.deepcopy(state)
          deck = [item for item in unknown if item not in i]
          newstate.deck = [Card(k[1], k[0]) for k in deck]
          newstate.Player2.cards = [Card(k[1], k[0]) for k in i]
          
          self.states.append(newstate)
    



if __name__ == "__main__":
    states = firstTest()
    state1 = states[0]
    
    space = BeliefSpace(state1,4)
    for state in space.states:
        print(state.Player2.storeInfo())
        
    
    print(state1.Player1.storeInfo())   
    print(state.Player1.storeInfo())   
    


