# This file is for the card class
import Constants
import time
import requests
from collections import Counter

class Card():
    def __init__(self, cardName: str) -> None:
        # Scryfall API requests that you insert 50ms of delay between requests
        time.sleep(.05)
        self.cardName = cardName
        cardUrl = Constants.exactSearch + cardName
        self.response = requests.get(cardUrl)
        # TODO: check if this throws errors/add error handling
        self.cardJSON = self.response.json()
        self.costDict = self.setCost()
        self.CMC = self.setCMC()
        self.isLand = "Land" in self.cardJSON["type_line"]

    def setCost(self):
        symbols = ["W", "U", "B", "R", "G"]
        manaDict = {"C": 0, "W":0, "U":0, "B":0, "R":0, "G":0}
        manaString = self.cardJSON['mana_cost']
        for char in manaString:
            if char.isnumeric():
                manaDict["C"] += int(char)
            if char in symbols:
                manaDict[char] += 1
        return manaDict

    def setCMC(self):
        CMC = 0
        for element in self.costDict.values():
            CMC += element
        return CMC

class Deck():
    def __init__(self, cardStrList:list) -> None:
        self.cardNames = cardStrList
        self.setCardsList(self.cardNames)

    def setCardsList(self, cardStrList):
        cardsList = []
        manaCurve = {}
        colorIdentity = {"W":0, "U":0, "B":0, "R":0, "G":0}
        for cardStr in cardStrList:
            tempCard = Card(cardStr)
            cardsList.append(tempCard)
            # TODO: maybe check if the tempcard is a land here to decide if it should update the color identity of the deck
            self.updateManaCurve(tempCard, manaCurve)
            self.updateColorIdentity(tempCard, colorIdentity)
        self.cardsList = cardsList
        self.manaCurve = manaCurve
        self.colorIdentity = colorIdentity

    def updateColorIdentity(self, card, colorIdentity):
        for color in card.cardJSON['color_identity']:
            colorIdentity[color] += 1

    def updateManaCurve(self, card, manaCurve):
        if card.CMC not in manaCurve:
            manaCurve[card.CMC] = 1
        else:
            manaCurve[card.CMC] += 1

if __name__ == '__main__':
    cardsList = ["Esper Sentinel", "Glittering Wish"]
    testDeck = Deck(cardsList)
    print("hello")