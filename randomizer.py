import random


class Randomizer:
    attributeCodes = [b'\x00', b'\x01', b'\x02', b'\x03', b'\x04']
    zeroBytes = bytes(b'\x00\x00')

    def __init__(self, seedVal):
        self.seedVal = seedVal
        random.seed(a=self.seedVal)  # seed the random module
        self.cardList = list()  # member: [cardID, get-card ID, card name]
        self.startingDeckList = list()  # member: [memory address, memory address,...]
        self.chestList = list()  # member: [memory address, level name, in-level location]
        self.hiddenList = list()  # member: [memory address, level name, in-level location]
        self.levelBonusList = list()  # member: [memory address,...]
        self.enemyAttributeList = list()  # member: memory address
        self.deckPointsList = list()  # member: memory address
        self.outputDict = dict()  # key: address val: randomized value
        self.optionLog = 'Options:\n'
        self.randLog = str()

    def start(self):
        if len(self.startingDeckList) > 0:
            self.optionLog += 'Randomized starting deck\n'
            self.randomizeStartingDeck()
        if len(self.chestList) > 0:
            self.optionLog += 'Randomized chest cards\n'
            self.randomizeCardLocationValues(self.chestList)
        if len(self.hiddenList) > 0:
            self.optionLog += 'Randomized hidden cards\n'
            self.randomizeCardLocationValues(self.hiddenList)
        if len(self.levelBonusList) > 0:
            self.optionLog += 'Randomized level bonus cards\n'
            self.randomizeLevelBonusCards()
        if len(self.enemyAttributeList) > 0:
            self.optionLog += 'Randomized enemy attributes\n'
            self.randomizeAttributes()
        if len(self.deckPointsList) > 0:
            self.optionLog += 'Deactivated deck points\n'
            self.deactivateDeckPoints()
        return self.outputDict, self.optionLog, self.randLog  # return tuple

    def randomizeStartingDeck(self):
        self.randLog += 'Starting Deck: '
        for cardSlot in self.startingDeckList:
            index = random.randint(0, len(self.cardList) - 1)  # choose random index to pull from cardIDs
            card = self.cardList[index]
            for address in cardSlot:
                self.outputDict[address] = card[0]
            amount = str((len(cardSlot) - 1))
            self.randLog += (card[2] + ' x' + amount + '. ')  # print card name
        self.randLog += '\n\n'

    def randomizeCardLocationValues(self, listToRandomize):
        for location in listToRandomize:
            index = random.randint(0, len(self.cardList) - 1)  # choose random index to pull from cardIDs
            card = self.cardList[index]
            self.outputDict[location[0]] = card[1]  # pair up location and get-card ID
            self.randLog += (location[1] + ' ' + location[2] + ' has ' + card[2] + '\n')  # (Level name) (location) has (card name)

    def randomizeLevelBonusCards(self):
        for cardSlot in self.levelBonusList:
            for address in cardSlot:
                index = random.randint(0, len(self.cardList) - 1)  # choose random index to pull from cardIDs
                card = self.cardList[index]
                self.outputDict[address] = card[0]

    def randomizeAttributes(self):
        for address in self.enemyAttributeList:
            attributeIndex = random.randint(0, len(self.attributeCodes) - 1)  # choose random attribute
            self.outputDict[address] = self.attributeCodes[attributeIndex]

    def deactivateDeckPoints(self):
        for address in self.deckPointsList:
            self.outputDict[address] = self.zeroBytes

    def setCardsList(self, cardData):
        self.cardList = cardData

    def setStartingDeckList(self, startingDeckData):
        self.startingDeckList = startingDeckData

    def setChestList(self, chestData):
        self.chestList = chestData

    def setHiddenList(self, hiddenData):
        self.hiddenList = hiddenData

    def setLevelBonusList(self, levelBonusData):
        self.levelBonusList = levelBonusData

    def setEnemyAttributeList(self, enemyAttributeData):
        self.enemyAttributeList = enemyAttributeData

    def setDeckPointsList(self, deckPointsData):
        self.deckPointsList = deckPointsData
