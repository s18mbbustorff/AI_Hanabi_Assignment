# -*- coding: utf-8 -*-
"""
Created on Mon Mar  8 15:39:18 2021

@author: mbust
"""
import numpy as np
from random import *
import copy


class State():
    def __init__(self, Player1, Player2, deck, playedPile, discardPile, hintTokens, penaltyTokens, turn, parent):
        self.Player1 = Player1
        self.Player = self.Player1
        self.Player2 = Player2
        self.AI = self.Player2
        self.deck = deck
        self.playedPile = playedPile
        self.discardPile = discardPile
        self.hintTokens = hintTokens
        self.penaltyTokens = penaltyTokens
        self.turn = turn
        
        self.parent = parent
        self.depth = 0
        self.value = 0
        self.test = "KUBA"
        
    def switchTurn(self):
        self.turn = self.turn%2 + 1
        
    def display(self):
        score = 0
        for s in self.playedPile.piles:
            score = len(s) + score            
        
        print ("Score : {}. Hint tokens left : {}, Penalty tokens used : {}. Cards left in the deck : {}.\n".format(score, self.hintTokens.numberOfTokens, self.penaltyTokens.numberOfTokens, len(self.deck.cards)))

        red = ';'.join([str(1), str(31), str(28)])
        blue = ';'.join([str(1), str(34), str(28)])
        green = ';'.join([str(1), str(39), str(42)])
        yellow = ';'.join([str(1), str(28), str(43)])
        white = ';'.join([str(1), str(37), str(40)])
        
        if self.playedPile.numberOfColors > 0:
            print ("Played Cards : \x1b[%sm %s \x1b[0m" % (red, self.playedPile.convertList(0)), end=" ")
        if self.playedPile.numberOfColors >= 2:
            print ('\x1b[%sm %s \x1b[0m' % (blue, self.playedPile.convertList(1)), end=" ")
        if self.playedPile.numberOfColors >= 3:
            print ('\x1b[%sm %s \x1b[0m' % (green, self.playedPile.convertList(2)), end=" ")
        if self.playedPile.numberOfColors >= 4:
            print ('\x1b[%sm %s \x1b[0m' % (yellow, self.playedPile.convertList(3)), end=" ")
        if self.playedPile.numberOfColors == 5:
            print ('\x1b[%sm %s \x1b[0m' % (white, self.playedPile.convertList(4)))
            print ('\n')
            
        print ("Discarded Cards : ", end=" ") 
        discardedPrint = self.discardPile.convertList()
        for card in discardedPrint:
            print(card, end="")
        print("")
    
    
                
class Action():
    
    def hint(initialState, hintType, hint):
        #hintType: String. Can be "number" or "color"
        #hint: String ("red","green",...) or Int ("1","2","3","4" or "5")
        
        #initializing variables (extracted from state)
        newState = copy.deepcopy(initialState)
        newState.parent = initialState
        newState.depth = initialState.depth+1
        
        if newState.turn == 1:
            activePlayer = newState.Player1
            otherPlayer = newState.Player2
        elif newState.turn == 2:
            activePlayer = newState.Player2
            otherPlayer = newState.Player1
        hintTokens = newState.hintTokens
        
        
        if hintTokens.numberOfTokens == 0:
            print ("Error. Number of Hint Tokens is 0. You cannot make a Hint.")
            return None
        
        if otherPlayer.allHintsGiven(hint, hintType):
            print ("Error. Hint already given or no cards correspond to the hint. You cannot make that hint.")
            return None
            
        for i in range(len(otherPlayer.cards)):
            if hintType == "color":
                if otherPlayer.cards[i].color == hint:
                    otherPlayer.cards[i].colorHinted = True
            elif hintType == "number":
                if otherPlayer.cards[i].number == hint:
                    otherPlayer.cards[i].numberHinted = True
        
        hintTokens.removeT()
                    
        newState.switchTurn()
        
        return newState
        
    def discard(initialState, cardPosition):
        #cardPosition: Int. Index of the card you want to discard from your hand.
        
        #initializing variables (extracted from state)
        newState = copy.deepcopy(initialState)
        newState.parent = initialState
        newState.depth = initialState.depth+1
        
        if newState.turn == 1:
            activePlayer = newState.Player1
        elif newState.turn == 2:
            activePlayer = newState.Player2
        hintTokens = newState.hintTokens
        deck = newState.deck
        discardPile = newState.discardPile
        
        if (hintTokens.numberOfTokens == hintTokens.maxTokens):
            print ("Error. Number of Hint Tokens is maxed. You cannot discard a card.")
            return None
        print("card discarded.1")
        discardedCard = activePlayer.cards[cardPosition]
        discardPile.addCard(discardedCard)
        print("card discarded.2")
        activePlayer.draw(deck, cardPosition)
        hintTokens.addT()
        
        newState.switchTurn()
        
        return newState
    
    
    
        
    def play(initialState, cardPosition):
        #cardPosition: Int. Index of the card you want to play from your hand.
        
        #initializing variables (extracted from state)
        newState = copy.deepcopy(initialState)
        newState.parent = initialState
        newState.depth = initialState.depth+1
        
        if newState.turn == 1:
            activePlayer = newState.Player1
        elif newState.turn == 2:
            activePlayer = newState.Player2
        penaltyTokens = newState.penaltyTokens
        deck = newState.deck
        
        playedCard = activePlayer.cards[cardPosition]
        
        #check if the card was correct somehow
        #use functions from the playPile
        verif = newState.playedPile.addCard(playedCard)
        
        if verif == False:
            newState.penaltyTokens.addT()
            newState.discardPile.addCard(playedCard)
            print("OOPS. You got a penalty token!")
            
        activePlayer.draw(deck, cardPosition)
        
        newState.switchTurn()
            
        return newState



class Player():
    
    #-----------------------------
    #-----Initialization functions
    #-----------------------------
    
    def __init__(self,name,order,numberOfCards):
        self.name = name
        self.order = order
        self.cards = [Card(None,0)]*numberOfCards
        self.numberOfCards = numberOfCards
        
    def setCards(self,cards):
        self.cards(cards)
        
    
    def drawNewHand(self, deck):
        #print("nb of cards:", len(self.cards))
        for i in range(len(self.cards)):
            self.draw(deck,i)
        
    #-----------------------------
    #-------------Action functions
    #-----------------------------
        
    #-------DISCARD---------------
    
    '''
    def discard(self,discardPile, cardPosition, hintTokens):
        if (hintTokens.nbTokens == hintTokens.maxTokens):
            print ("Error. Number of Hint Tokens is maxed. You cannot discard a card.")
            return None
        discardedCard = self.cards[cardPosition]
        discardPile.addCard(discardedCard)
        newCard = self.draw(cardPosition)
        self.cards[ardPosition] = newCard
        hintTokens.addT()
        return newCard
    '''
    def draw(self,deck, cardPosition):
        newCard = deck.removeRandom()
        #print("pos: {}, color: {}, nb: {}".format(cardPosition, newCard.color,newCard.number))
        self.cards[cardPosition] = newCard
        return newCard
        
    #-----------HINT--------------
    
    '''
    def hint(self, player, hintType, hint, hintTokens):
        if hintTokens == 0:
            print ("Error. Number of Hint Tokens is 0. You cannot make a Hint.")
            return None
        
        if player.allHintsGiven(hint, hintType):
                print ("Error. Hint already given or no cards correspond to the hint. You cannot make that hint.")
                return
            
        for i in range(len(player.cards)):
            if hintType == "color":
                if player.cards[i].color == hint:
                    player.cards[i].colorHinted = True
            elif hintType == "number":
                if player.cards[i].number == hint:
                    player.cards[i].numberHinted = True
    ''' 
    
    def allHintsGiven(self, hint, hintType):
        if hint is None:
            for i in range(len(self.cards)):
                if (self.cards[i].colorHinted == False) or (self.cards[i].numberHinted == False):
                    return False
            return True
        elif hintType == "color":
            for i in range(len(self.cards)):
                if (self.cards[i].color == hint) and (self.cards[i].colorHinted == False):
                    return False
            return True
            
        elif hintType == "number":
            for i in range(len(self.cards)):
                if (self.cards[i].number == hint) and (self.cards[i].numberHinted == False):
                    return False
            return True
    
    '''
    def playCard(self, playPile, cardPosition, deck, penaltyTokens):
        playedCard = self.cards[cardPosition]
        
        #check if the card was correct somehow
        #use functions from the playPile
        
        self.draw(deck, cardPosition)
    '''   
    
    #-----------------------------
    #------Visualization functions
    #-----------------------------
    
    def storeInfo(self):
       # Declaring rows 
       N = len(self.cards)
       # Declaring columns 
       M = 2
       # using list comprehension  
       # to initializing matrix 
       cardMatrix = [ [ 0 for i in range(M) ] for j in range(N) ] 
       
       for i in range(len(self.cards)):
           number = str(self.cards[i].number)
           color = str(self.cards[i].color)
           if self.cards[i].numberHinted:
               number = number+"*"
           if self.cards[i].colorHinted:
               color = color+"*"
               
           cardMatrix[i][0] = number
           cardMatrix[i][1] = color
       
       return cardMatrix
     

class Card():
    
    #-----------------------------
    #-----Initialization functions
    #-----------------------------
    
    def __init__(self,color,number):
        self.color = color
        self.number = number
        self.colorHinted = False
        self.numberHinted = False
    
    #-----------------------------
    #------Visualization functions
    #-----------------------------
    
    def sayInfo(self):
        print ("Color: {}, number: {}.".format(self.color,self.number))
        
    def __eq__(self, other):
       
        return self.__dict__ == other.__dict__

class Deck():
    
    #-----------------------------
    #-----Initialization functions
    #-----------------------------
    
    def __init__(self,numberOfColors,cardsDistribution):
        #var cardsDistribution = int list of 1,2,3,4,5s
        self.numberOfColors = numberOfColors
        #var numberOfColors = int
        self.cardsDistribution = cardsDistribution
        #creating the initial deck of cards with all available cards in it
        cards=[]
        cardsPerColor = len(cardsDistribution)
        colorPossibilities = np.array(["red","blue","green","yellow","white"])[:numberOfColors]
        cardNumbers = cardsDistribution * numberOfColors
        for i in range(len(cardNumbers)):
                color = colorPossibilities[i//cardsPerColor]
                number = cardNumbers[i]
                cards.append(Card(color,number))
            
        self.cards = cards
        self.numberOfCards = len(cards)
        
    def __intit__(self,cards):
        self.cards = cards
        
    #------------------------------
    #---Draw/remove cards functions
    #------------------------------
    
    def removeRandom(self):
        maxIndex =len(self.cards)-1
        randomIndex =(randrange(maxIndex))
        randomCard = self.cards[randomIndex]
        self.cards.pop(randomIndex)
        self.numberOfCards = len(self.cards)
        return randomCard
    
    def removeCard(self,cardToRemove):
        for i in range(self.numberOfCards):
            if cardToRemove.isSameAs(self.cards[i]):
                del self.cards[i]
                self.numberOfCards =- 1
                break
        return self.numberOfCards
    
    #-----------------------------
    #------Visualization functions
    #-----------------------------
    
    def sayAllCards(self):
        for i in range(len(self.cards)):
            self.cards[i].sayInfo()
            
    def storeInfo(self):
        # Declaring rows 
        N = len(self.cards)
        # Declaring columns 
        M = 2
        # using list comprehension  
        # to initializing matrix 
        cardMatrix = [ [ 0 for i in range(M) ] for j in range(N) ] 
        
        for i in range(len(self.cards)):
            cardMatrix[i][0] = self.cards[i].number
            cardMatrix[i][1] = str(self.cards[i].color)
        
        return cardMatrix
            
            
class DiscardPile():
    
    def __init__(self, cards):
        self.cards = cards
        self.numberOfCards = len(cards)
        
    def addCard(self, card):
        self.cards.append(card)
        self.numberOfCards += 1
        return self.numberOfCards
    
    def convertList(self):
        
        red = ';'.join([str(1), str(31), str(28)])
        blue = ';'.join([str(1), str(34), str(28)])
        green = ';'.join([str(1), str(39), str(42)])
        yellow = ';'.join([str(1), str(28), str(43)])
        white = ';'.join([str(1), str(37), str(40)])
        
        listCards = []
        for i in range(len(self.cards)):
            
            currentCard = self.cards[i]
            if currentCard.color == "red":
                coloredCardNumber = '\x1b[%sm %s \x1b[0m' % (red, currentCard.number)
            elif currentCard.color == "blue":
                coloredCardNumber = '\x1b[%sm %s \x1b[0m' % (blue, currentCard.number)
            elif currentCard.color == "green":
                coloredCardNumber = '\x1b[%sm %s \x1b[0m' % (green, currentCard.number)
            elif currentCard.color == "yellow":
                coloredCardNumber = '\x1b[%sm %s \x1b[0m' % (yellow, currentCard.number)
            elif currentCard.color == "white":
                coloredCardNumber = '\x1b[%sm %s \x1b[0m' % (white, currentCard.number)
            listCards += [coloredCardNumber]
            
        return listCards
            
        
class PlayedPile():
    
    def __init__(self, numberOfColors):
        self.colors = ["red", "blue", "green", "yellow", "white"][:numberOfColors]
        self.numberOfColors = numberOfColors
        self.piles = [[] for i in range(self.numberOfColors)]   ## Lists (representing each pile) within a list 
        
    def addCard(self, card):
        if card.color in self.colors:
            pileIndex = self.colors.index(card.color)
            
            if (len(self.piles[pileIndex]) == 0) and (card.number == 1):
                self.piles[pileIndex].append(card)
                
            elif (len(self.piles[pileIndex]) != 0) and (card.number == self.piles[pileIndex][-1].number + 1):
                self.piles[pileIndex].append(card)
                
            else:
                print ("Error. Card not matched to any pile. Could not add the card to a pile")
                return False
            
            print("Well done! The card was added to the firework!")
            self.piles[pileIndex][-1].sayInfo()
            return True
            
        else:
            print ("Error. Card color does not exist. Could not add the card to a pile")
    
    def convertList(self, pilePosition):
        listCards = []
        for i in range(len(self.piles[pilePosition])):
            listCards += [self.piles[pilePosition][i].number]
        return listCards
    
class HintTokens():
    
    def __init__(self, numberOfTokens, maxTokens):
        self.numberOfTokens = numberOfTokens
        self.maxTokens = maxTokens
        
    def removeT(self):
        if 0 < self.numberOfTokens:
            self.numberOfTokens -= 1
        else:
            print ("Error. Not enough tokens. Could not remove the hint token.")
       
    def addT(self):
        if self.numberOfTokens < self.maxTokens:
            self.numberOfTokens += 1
        else:
            print ("Error. Tokens maximum limit reached. Could not add the hint token.")
        
        
class PenaltyTokens():
    
    def __init__(self, numberOfTokens, maxTokens):
        self.numberOfTokens = numberOfTokens
        self.maxTokens = maxTokens
        
    def removeT(self):
        if 0 < self.numberOfTokens:
            self.numberOfTokens -= 1
        else:
            print ("Error. Not enough tokens. Could not remove the penalty token.")
       
    def addT(self):
        if self.numberOfTokens < self.maxTokens:
            self.numberOfTokens += 1
        else:
            print ("Error. Tokens maximum limit reached. Could not add the penalty token.")
    