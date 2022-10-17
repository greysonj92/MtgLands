# This file is for the card class
import Constants
import time
import requests
import os
import logging
import random
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

    def __repr__(self):
        return self.cardName

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
        manaCurve = {"0": 0,"1": 0,"2": 0,"3": 0,"4": 0,"5": 0,"6": 0,"7": 0,"8": 0,"9+": 0,}
        colorIdentity = {"W":0, "U":0, "B":0, "R":0, "G":0}
        logging.info("Starting Scryfall query for cards in deck list, this will take some time.\n")
        firstTimestamp = time.time()
        for cardStr in cardStrList:
            logging.info(f"Adding card {cardStr} to deck.")
            tempCard = Card(cardStr)
            cardsList.append(tempCard)
            # TODO: maybe check if the tempcard is a land here to decide if it should update the color identity of the deck
            self.updateManaCurve(tempCard, manaCurve)
            self.updateColorIdentity(tempCard, colorIdentity)
        secondTimestamp = time.time()
        logging.info(f"Took {secondTimestamp - firstTimestamp} seconds to query Scryfall for deck list.")
        self.cardsList = cardsList
        self.manaCurve = manaCurve
        self.colorIdentity = colorIdentity

    def updateColorIdentity(self, card, colorIdentity):
        for color in card.cardJSON['color_identity']:
            colorIdentity[color] += 1

    def updateManaCurve(self, card, manaCurve):
        if card.isLand:
            pass
        elif card.CMC < 9:
            manaCurve[str(card.CMC)] += 1
        else:
            manaCurve["9+"] += 1

    def setWithoutLands(self):
        self.withoutLands = []
        for card in self.cardsList:
            if not card.isLand:
                self.withoutLands.append(card)

    def drawHand(self):
        self.hand = random.sample(self.cardsList, 7)
        lands = []
        nonLands = []
        for item in self.hand:
            if item.isLand:
                lands.append(item)
            else:
                nonLands.append(item)
        print("\n===================================")
        print("Lands:\n")
        for item in lands:
            print(item)
        print("\n===================================")
        print("Non-Lands:\n")
        for item in nonLands:
            print(item)
    def markovChain(self, iterations:int):
        landsInHand = {"0": 0,"1": 0,"2": 0,"3": 0,"4": 0,"5": 0,"6": 0,"7": 0}
        logging.info("Starting Markov Chain.")
        firstTimestamp = time.time()
        for i in range(iterations):
            landCounter = 0
            hand = random.sample(self.cardsList, 7)
            for card in hand:
                if card.isLand:
                    landCounter += 1
                else:
                    pass
            landsInHand[str(landCounter)] += 1
        secondTimestamp = time.time()
        logging.info(f"Time to run Markov chain: {secondTimestamp - firstTimestamp} seconds.")
        logging.info(f"Ran {iterations} iterations")
        for element in landsInHand.items():
            print(f"Number of {element[0]} land hands: {element[1]} proportion: {element[1]/iterations}")



if __name__ == '__main__':
    # test reading a decklist from file
    logging.basicConfig(level=logging.INFO)
    deckList = []
    print(os.getcwd())
    fileName = os.path.join(os.getcwd(), r"src\testDecks\Deck - Ur-Dragon.txt")
    with open(fileName, "r") as file:
        for line in file:
            tempStr = line[2:]
            tempStr = tempStr.rstrip()
            if len(tempStr) > 0:
                deckList.append(tempStr)

    testDeck = Deck(deckList)
    print("Your deck's mana curve:\n")
    for i in sorted(testDeck.manaCurve.keys()):
        tempBar = ""
        for j in range(testDeck.manaCurve[i]):
            tempBar += "|"
        print(i,": ", tempBar, testDeck.manaCurve[i])
    testDeck.markovChain(1000000)