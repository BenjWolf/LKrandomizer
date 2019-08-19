import os
import classes


class FileLoad:
    # file names
    cardIDFile = 'data/cardID.csv'
    itemIDFile = 'data/itemID.csv'
    startingDeckFile = 'data/startingDeckAddress.csv'
    chestCardItemFile = 'data/chestCardItem.csv'
    warriorWyhtFile = 'data/warriorWyhtAddress.txt'
    levelBonusCardFile = 'data/levelBonusAddress.csv'
    shopCardFile = 'data/shopCardAddress.txt'
    fairyCardFile = 'data/fairyCardAddress.txt'
    enemyAttributeFile = 'data/enemyAttributeAddress.txt'
    deckPointFile = 'data/deckPointAddress.txt'
    summonCardFile = 'data/summonCardAddress.txt'
    savedPathFile = 'data/savedPath.txt'

    # constants
    isoSize = 1459978240
    gameID = bytes(b'GRNE52')

    def __init__(self):  # todo add exception for file loads?
        self.cardList = list()  # member: card object
        self.loadCards()
        self.itemList = list()  # member: [itemID, item name]
        self.loadItems()
        self.startingDeckList = list()  # member: [memory address, memory address,...]
        self.loadStartingDeck()
        self.chestCardItemList = list()  # member: [memory address, type, area, level name, location desc]
        self.loadChestCardItem()
        self.warriorWyhtList = list() # member: memory address
        self.loadWarriorWyht()
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
        self.summonList = list()  # member: [memory address, cardType]
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

    def loadCards(self):  # todo check if converting to bytes is necessary
        # load [card ID, interact ID, card name, rarity] from file into cards list
        with open(self.cardIDFile, 'r') as file:
            lines = file.readlines()
            for line in lines:
                line = line.rstrip('\r\n')
                line = line.split(',')
                line[0] = self.convertFromStringToInt16(line[0])
                line[0] = (line[0]).to_bytes(1, byteorder='big')  # to bytes
                line[1] = self.convertFromStringToInt16(line[1])
                line[1] = (line[1]).to_bytes(1, byteorder='big')  # to bytes
                card = classes.Card(line[0], line[1], line[2], line[3])
                self.cardList.append(card)

    def loadItems(self):
        # load [item ID, card name] from file into cards list
        with open(self.itemIDFile, 'r') as file:
            lines = file.readlines()
            for line in lines:
                line = line.rstrip('\r\n')
                line = line.split(',')
                line[0] = self.convertFromStringToInt16(line[0])
                line[0] = (line[0]).to_bytes(1, byteorder='big')  # to bytes
                item = classes.Item(line[0], line[1])
                self.itemList.append(item)

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
        # load [memory address, type, area, level name, location desc] from file into locations list
        with open(self.chestCardItemFile, 'r') as file:
            lines = file.readlines()
            for line in lines:
                line = line.rstrip('\r\n')
                line = line.split(',')
                line[0] = self.convertFromStringToInt16(line[0])
                line[1] = int(line[1])
                line[2] = int(line[2])
                if not line[5] == '':
                    line[5] = self.convertFromStringToInt16(line[5])
                    location = classes.Location(line[0], line[1], line[2], line[3], line[4], line[5])
                else:
                    location = classes.Location(line[0], line[1], line[2], line[3], line[4])
                self.chestCardItemList.append(location)

    def loadWarriorWyht(self):
        self.loadAddressTxtFile(self.warriorWyhtFile, self.warriorWyhtList)

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
        with open(self.summonCardFile, 'r') as file:
            lines = file.readlines()
            for line in lines:
                line = line.rstrip('\r\n')
                line = line.split(',')
                line[0] = self.convertFromStringToInt16(line[0])
                line[1] = self.convertFromStringToInt16(line[1])
                line[1] = (line[1]).to_bytes(1, byteorder='big')  # to bytes
                summon = classes.Summon(line[0], line[1])
                self.summonList.append(summon)

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
