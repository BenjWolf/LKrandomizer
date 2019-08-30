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
    lk2CardFile = 'data/lk2Card.csv'
    lk2EnemyFile = 'data/lk2Enemy.csv'
    # summonCardFile = 'data/summonCardAddress.txt'
    savedPathFile = 'data/savedPath.txt'

    # constants
    isoSize = 1459978240
    gameID = bytes(b'GRNE52')

    def __init__(self):  # todo add exception for file loads?
        self.cardList = list()  # member: card object
        self.loadCards()
        self.itemList = list()  # member: [itemID, item name]
        self.loadItems()
        self.startingDeckList = list()  # member: [.iso address, .iso address,...]
        self.loadStartingDeck()
        self.chestCardItemList = list()  # member: [.iso address, type, area, level name, location desc]
        self.loadChestCardItem()
        self.warriorWyhtList = list() # member: .iso address
        self.loadWarriorWyht()
        self.levelBonusList = list()  # member: [.iso address,...]
        self.loadLevelBonusCards()
        self.shopCardList = list()  # member: .iso address
        self.loadShopCards()
        self.fairyCardList = list()  # member: .iso address
        self.loadFairyCards()
        self.enemyAttributeList = list()  # member: .iso address
        self.loadEnemyAttributes()
        self.deckPointList = list()  # member: .iso address
        self.loadDeckPoints()
        self.lk2CardChangeList = list()  # member: .iso address, new value (int, limit 1 byte)
        self.loadlk2CardChanges()
        self.lk2EnemyChangeList = list()  # member: .iso address, new value (int, limit 2 bytes)
        self.loadlk2EnemyChanges()
        '''        
        self.summonList = list()  # member: [.iso address, cardType]
        self.loadSummonCards()
        '''

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
                line[0] = int(line[0], 16)
                line[0] = line[0].to_bytes(1, byteorder='big')
                line[1] = int(line[1], 16)
                line[1] = line[1].to_bytes(1, byteorder='big')
                card = classes.Card(line[0], line[1], line[2], line[3])
                self.cardList.append(card)

    def loadItems(self):
        # load [item ID, card name] from file into cards list
        with open(self.itemIDFile, 'r') as file:
            lines = file.readlines()
            for line in lines:
                line = line.rstrip('\r\n')
                line = line.split(',')
                line[0] = int(line[0], 16)
                line[0] = line[0].to_bytes(1, byteorder='big')
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
                    address = int(address, 16)
                    cardAddresses.append(address)
                self.startingDeckList.append(cardAddresses)

    def loadChestCardItem(self):
        # load [.iso address, type, area, level name, location desc] from file into locations list
        with open(self.chestCardItemFile, 'r') as file:
            lines = file.readlines()
            for line in lines:
                line = line.rstrip('\r\n')
                line = line.split(',')
                line[0] = int(line[0], 16)
                line[1] = int(line[1])
                line[2] = int(line[2])
                line[5] = int(line[5], 16)
                line[5] = line[5].to_bytes(1, byteorder='big')
                if not line[6] == '':  # has type address
                    line[6] = int(line[6], 16)
                    location = classes.Location(line[0], line[1], line[2], line[3], line[4], line[5], line[6])
                else:
                    location = classes.Location(line[0], line[1], line[2], line[3], line[4], line[5])
                self.chestCardItemList.append(location)

    def loadWarriorWyht(self):
        self.loadAddressTxtFile(self.warriorWyhtFile, self.warriorWyhtList)

    def loadLevelBonusCards(self):
        with open(self.levelBonusCardFile, 'r') as file:
            lines = file.readlines()
            for line in lines:
                line = line.rstrip('\r\n')
                line = line.split(',')
                addresses = line[0].split('.')
                newAdresses = list()
                for address in addresses:
                    address = int(address, 16)
                    newAdresses.append(address)
                line[1] = int(line[1], 16)
                line[1] = line[1].to_bytes(1, byteorder='big')
                levelBonusSlot = classes.LevelBonusSlot(newAdresses, line[1])
                self.levelBonusList.append(levelBonusSlot)

    def loadShopCards(self):
        self.loadAddressTxtFile(self.shopCardFile, self.shopCardList)

    def loadFairyCards(self):
        self.loadAddressTxtFile(self.fairyCardFile, self.fairyCardList)

    def loadEnemyAttributes(self):
        self.loadAddressTxtFile(self.enemyAttributeFile, self.enemyAttributeList)

    def loadDeckPoints(self):
        self.loadAddressTxtFile(self.deckPointFile, self.deckPointList)

    def loadlk2CardChanges(self):
        self.loadReplaceBytesFile(self.lk2CardFile, self.lk2CardChangeList, 1)

    def loadlk2EnemyChanges(self):
        self.loadReplaceBytesFile(self.lk2EnemyFile, self.lk2EnemyChangeList, 2)

    def loadAddressTxtFile(self, fileName, intoList):
        with open(fileName, 'r') as file:
            lines = file.readlines()
            for address in lines:
                address = address.rstrip('\r\n')
                address = int(address, 16)
                intoList.append(address)

    def loadReplaceBytesFile(self, fileName, intoList, numBytes):
        with open(fileName, 'r') as file:
            lines = file.readlines()
            for line in lines:
                line = line.rstrip('\r\n')
                line = line.split(',')
                line[0] = int(line[0], 16)
                line[1] = int(line[1])
                line[1] = line[1].to_bytes(numBytes, byteorder='big')  # values have lengths of two bytes
                replaceBytes = classes.ReplaceBytes(line[0], line[1])
                intoList.append(replaceBytes)