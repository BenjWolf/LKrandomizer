import os


class FileLoad:
    # file names
    cardIDFile = 'data/cardID.csv'  # todo add rarity field
    startingDeckFile = 'data/startingDeckAddress.csv'
    chestCardItemFile = 'data/chestCardItem.csv'
    levelBonusCardFile = 'data/levelBonusAddress.csv'
    shopCardFile = 'data/shopCardAddress.txt'
    fairyCardFile = 'data/fairyCardAddress.txt'
    enemyAttributeFile = 'data/enemyAttributeAddress.txt'
    deckPointFile = 'data/deckPointAddress.txt'
    summonCardFile = 'data/summonCardAddress.txt'  # todo might change file to have another field
    savedPathFile = 'data/savedPath.txt'

    # constants
    isoSize = 1459978240
    gameID = bytes(b'GRNE52')

    def __init__(self):  # todo add exception for file loads?
        self.cardList = list()  # member: [cardID, get-card ID, card name]
        self.loadCardData()
        self.startingDeckList = list()  # member: [memory address, memory address,...]
        self.loadStartingDeck()
        self.chestCardItemList = list()  # member: [memory address, type, availability, level name, location desc]
        self.loadChestCardItem()
        self.levelBonusList = list()  # member: [memory address,...]
        self.loadLevelBonusCards()
        self.shopCardList = list()  # member: memory address
        self.loadShopCards()
        self.fairyCardList = list()  # member: memory address
        self.loadFairyCards()
        self.enemyAttributeList = list()  # member: memory address
        self.loadEnemyAttributes()
        self.deckPointList = list()  # member: memory address
        self.loadDeckPoints()
        self.summonList = list()  # member: memory address
        self.loadSummonCards()

    def loadSavedFilePath(self):
        with open(self.savedPathFile, 'r') as file:
            savedPath = file.read()
        return savedPath

    def isGoodISO(self, ISOPath):
        if os.path.getsize(ISOPath) != self.isoSize:
            return False
        with open(ISOPath, 'rb') as iso_file:
            if iso_file.read(6) != self.gameID:
                return False
        return True

    def loadCardData(self):  # todo check if converting to bytes is necessary
        # load [card ID, card-get ID, card name] from file into cards list
        with open(self.cardIDFile, 'r') as file:
            lines = file.readlines()
            for line in lines:  # todo use enumerate in for loops?
                line = line.rstrip('\r\n')
                card = line.split(',')  # [id, card-get ID, card name]
                card[0] = self.convertFromStringToInt16(card[0])
                card[0] = (card[0]).to_bytes(1, byteorder='big')  # to bytes
                card[1] = self.convertFromStringToInt16(card[1])
                card[1] = (card[1]).to_bytes(1, byteorder='big')  # to bytes
                self.cardList.append(card)

    def loadStartingDeck(self):
        with open(self.startingDeckFile, 'r') as file:
            lines = file.readlines()
            for line in lines:
                line = line.rstrip('\r\n')
                card = line.split(',')
                cardAddresses = list()
                for address in card:
                    address = self.convertFromStringToInt16(address)
                    cardAddresses.append(address)
                self.startingDeckList.append(cardAddresses)

    def loadChestCardItem(self):
        # load [memory address, type, availability, level name, location desc] from file into locations list
        with open(self.chestCardItemFile, 'r') as file:
            lines = file.readlines()
            for line in lines:
                line = line.rstrip('\r\n')
                location = line.split(',')
                location[0] = self.convertFromStringToInt16(location[0])
                location[1] = int(location[1])
                self.chestCardItemList.append(location)

    def loadLevelBonusCards(self):
        with open(self.levelBonusCardFile, 'r') as file:
            lines = file.readlines()
            for line in lines:
                line = line.rstrip('\r\n')
                card = line.split(',')
                cardAddresses = list()
                for address in card:
                    address = self.convertFromStringToInt16(address)
                    cardAddresses.append(address)
                self.levelBonusList.append(cardAddresses)

    def loadShopCards(self):
        self.loadAddressTxtFile(self.shopCardFile, self.shopCardList)

    def loadFairyCards(self):
        self.loadAddressTxtFile(self.fairyCardFile, self.fairyCardList)

    def loadEnemyAttributes(self):
        self.loadAddressTxtFile(self.enemyAttributeFile, self.enemyAttributeList)

    def loadDeckPoints(self):
        self.loadAddressTxtFile(self.deckPointFile, self.deckPointList)

    def loadSummonCards(self):
        self.loadAddressTxtFile(self.summonCardFile, self.summonList)

    def loadAddressTxtFile(self, fileName, intoList):
        with open(fileName, 'r') as file:
            lines = file.readlines()
            for address in lines:
                address = address.rstrip('\r\n')
                address = self.convertFromStringToInt16(address)
                intoList.append(address)

    def convertFromStringToInt16(self, string):
        int16 = int(string, 16)
        return int16

    def getCardList(self):
        return self.cardList

    def getStartingDeckList(self):
        return self.startingDeckList

    def getchestCardItemList(self):
        return self.chestCardItemList

    def getLevelBonusList(self):
        return self.levelBonusList

    def getShopCardList(self):
        return self.shopCardList

    def getFairyCardList(self):
        return self.fairyCardList

    def getEnemyAttributeList(self):
        return self.enemyAttributeList

    def getDeckPointList(self):
        return self.deckPointList

    def getSummonList(self):
        return self.summonList
