# This file is for the card class
import Constants
import time
import requests


class Card():
    def __init__(self, cardName: str) -> None:
        # Scryfall API requests that you insert 50ms of delay between requests
        time.sleep(.05)
        cardUrl = Constants.exactSearch + cardName
        response = requests.get(cardUrl)
        response.json()

if __name__ == '__main__':
    testCard = Card("Austere Command")
    