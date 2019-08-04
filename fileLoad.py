import os


class FileLoad:
    # file names
    cardIDFile = 'data/cardID.csv'
    startingDeckFile = 'data/startingDeckAddress.csv'
    chestAddressFile = 'data/chestAddress.csv'
    hiddenAddressFile = 'data/hiddenAddress.csv'
    levelBonusAddressFile = 'data/levelBonusAddress.csv'
    enemyAttributesFile = 'data/enemyAttributeAddress.txt'
    deckPointAddressFile = 'data/deckPointAddress.txt'
    savedPathFile = 'data/savedPath.txt'

    # constants
    isoSize = 1459978240
    gameID = bytes(b'GRNE52')

    def __init__(self):  # todo add exception for file loads?
        pass

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
        cardsList = list()
        with open(self.cardIDFile, 'r') as file:
            lines = file.readlines()
            for line in lines:  # todo use enumerate in for loops?
                line = line.rstrip('\r\n')
                card = line.split(',')  # [id,name]
                card[0] = self.convertFromStringToInt16(card[0])
                card[0] = (card[0]).to_bytes(1, byteorder='big')  # to bytes
                card[1] = self.convertFromStringToInt16(card[1])
                card[1] = (card[1]).to_bytes(1, byteorder='big')  # to bytes
                cardsList.append(card)
        return cardsList

    def loadStartingDeck(self):
        startingDeckList = list()
        with open(self.startingDeckFile, 'r') as file:
            lines = file.readlines()
            for line in lines:
                line = line.rstrip('\r\n')
                card = line.split(',')
                cardAddresses = list()
                for address in card:
                    address = self.convertFromStringToInt16(address)
                    cardAddresses.append(address)
                startingDeckList.append(cardAddresses)
        return startingDeckList

    def loadChests(self):
        # load [memory address, level name, in-level location] from file into locations list
        chestList = list()
        with open(self.chestAddressFile, 'r') as file:
            lines = file.readlines()
            for line in lines:
                line = line.rstrip('\r\n')
                location = line.split(',')
                location[0] = self.convertFromStringToInt16(location[0])
                chestList.append(location)
        return chestList

    def loadHiddenCards(self):
        # load [memory address, level name, in-level location] from file into locations list
        hiddenList = list()
        with open(self.hiddenAddressFile, 'r') as file:
            lines = file.readlines()
            for line in lines:
                line = line.rstrip('\r\n')
                location = line.split(',')
                location[0] = self.convertFromStringToInt16(location[0])
                hiddenList.append(location)
        return hiddenList

    def loadLevelBonusCards(self):
        levelBonusList = list()
        with open(self.levelBonusAddressFile, 'r') as file:
            lines = file.readlines()
            for line in lines:
                line = line.rstrip('\r\n')
                card = line.split(',')
                cardAddresses = list()
                for address in card:
                    address = self.convertFromStringToInt16(address)
                    cardAddresses.append(address)
                levelBonusList.append(cardAddresses)
        return levelBonusList

    def loadEnemyAttributes(self):
        enemyAttributesList = list()
        with open(self.enemyAttributesFile, 'r') as file:
            lines = file.readlines()
            for address in lines:
                address = address.rstrip('\r\n')
                address = self.convertFromStringToInt16(address)
                enemyAttributesList.append(address)
        return enemyAttributesList

    def loadDeckPoints(self):
        deckPointList = list()
        with open(self.deckPointAddressFile, 'r') as file:
            lines = file.readlines()
            for address in lines:
                address = address.rstrip('\r\n')
                address = self.convertFromStringToInt16(address)
                deckPointList.append(address)
        return deckPointList

    def convertFromStringToInt16(self, string):
        int16 = int(string, 16)
        return int16
