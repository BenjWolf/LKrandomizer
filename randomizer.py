import random


class Randomizer:
    attributeCodes = [b'\x00', b'\x01', b'\x02', b'\x03', b'\x00', b'\x01', b'\x02', b'\x03', b'\x04']  # doubled elemental attributes
    escapeBattleReplacement = {int(b'24A08', 16): bytes(b'\x60\x00\x00\x00')}
    zeroBytes = bytes(b'\x00\x00')
    heavyWeaponBytes = bytes(b'\x05')
    nopCode = bytes(b'\x60\x00\x00\x00')

    def __init__(self, seedVal):
        self.seedVal = seedVal
        random.seed(a=self.seedVal)  # seed the random module
        self.cardList = list()  # member: [cardID, get-card ID, card name]
        self.outputDict = dict()  # key: address val: randomized value
        self.optionLog = 'Options:\n'
        self.randLog = str()

    def randomizeStartingDeck(self, startingDeckList):
        self.optionLog += 'Randomized starting deck\n'
        self.randLog += 'Starting Deck: '
        for cardSlot in startingDeckList:  # cardSlot: [memory address, memory address,...]
            card = self.getRandomCard()
            for address in cardSlot:
                self.outputDict[address] = card[0]
            amount = str((len(cardSlot) - 1))
            self.randLog += (card[2] + ' x' + amount + '. ')  # print card name
        self.randLog += '\n\n'

    def randomizeChestCardItems(self, chestCardItemList, doChestCards, doHiddenCards):
        locationList = list(chestCardItemList)  # make copy of list
        if doChestCards:
            self.optionLog += 'Randomized chest cards\n'
        else:  # remove chest cards from list
            for member in chestCardItemList:
                if member[1] == 1:
                    locationList.remove(member)
        if doHiddenCards:
            self.optionLog += 'Randomized hidden cards\n'
        else:  # remove hidden cards from list
            deleteList = list()
            for member in chestCardItemList:
                if member[1] == 2:
                    locationList.remove(member)
        # todo item assignment here
        for location in locationList:
            card = self.getRandomCard()
            self.outputDict[location[0]] = card[1]  # pair up location and get-card ID
            self.randLog += (location[3] + ' ' + location[4] + ' has ' + card[2] + '\n')  # (Level name) (location) has (card name)
        self.randLog += '\n'

    def randomizeLevelBonusCards(self, levelBonusList):
        self.optionLog += 'Randomized level bonus cards\n'
        for cardSlot in levelBonusList:  # cardSlot: [memory address,...]
            for address in cardSlot:
                card = self.getRandomCard()
                self.outputDict[address] = card[0]

    def randomizeShopCards(self, shopCardList):
        self.optionLog += 'Randomized shop cards\n'
        self.randLog += 'Shop cards:\n'
        n = 0
        for address in shopCardList:
            n += 1
            card = self.getRandomCard()
            self.outputDict[address] = card[0]
            self.randLog += card[2] + '. '  # print card name
            if n % 10 == 0:  # every tenth card start new line
                self.randLog += '\n'
        self.randLog += '\n'

    def randomizeFairyCards(self, fairyCardList):
        self.optionLog += 'Randomized red fairy rewards\n'
        self.randLog += 'Red fairy rewards:\n'
        for address in fairyCardList:
            card = self.getRandomCard()
            self.outputDict[address] = card[0]
            self.randLog += card[2] + '. '  # print card name

    def randomizeAttributes(self, enemyAttributeList):
        self.optionLog += 'Randomized enemy attributes\n'
        for address in enemyAttributeList:  # member: memory address
            attributeIndex = random.randint(0, len(self.attributeCodes) - 1)  # choose random attribute
            self.outputDict[address] = self.attributeCodes[attributeIndex]

    def removeEscapeBattle(self):
        self.optionLog += 'Can\'t escape battles\n'
        self.outputDict.update(self.escapeBattleReplacement)

    def deactivateDeckPoints(self, deckPointsList):
        self.optionLog += 'Deactivated deck points\n'
        for address in deckPointsList:
            self.outputDict[address] = self.zeroBytes

    def removeSummonAnimations(self, summonList):
        self.optionLog += 'Removed summon animations\n'
        for address in summonList:  # member: memory address
            self.outputDict[address] = self.heavyWeaponBytes

    def getRandomCard(self):
        index = random.randint(0, len(self.cardList) - 1)  # choose random index to pull from cardIDs
        return self.cardList[index]

    def setCardsList(self, cardData):
        self.cardList = cardData

    def getRandomizerOutput(self):
        return self.outputDict, self.optionLog, self.randLog  # return tuple
