import random
import itemPlacer


class Randomizer:
    escapeBattleAddress = int(b'24A08', 16)
    attributeCodes = [b'\x00', b'\x01', b'\x02', b'\x03', b'\x00', b'\x01', b'\x02', b'\x03', b'\x04']  # doubled elemental attributes
    zeroBytes = bytes(b'\x00\x00')
    cardGetByte = b'\x66'
    itemGetByte = b'\x65'
    nopCode = bytes(b'\x60\x00\x00\x00')

    def __init__(self, seedVal):
        random.seed(a=seedVal)  # seed the random module
        self.cardList = list()  # member: card object
        self.outputDict = dict()  # key: address val: randomized value
        self.optionLog = 'Options:\n'
        self.spoilerLog = str()

    def randomizeStartingDeck(self, startingDeckList):
        self.optionLog += 'Randomized starting deck\n'
        self.spoilerLog += 'Starting Deck: '
        for cardSlot in startingDeckList:  # cardSlot: [memory address, memory address,...]
            card = self.getRandomCard()
            for address in cardSlot:
                self.outputDict[address] = card.cardID
            amount = str((len(cardSlot) - 1))
            self.spoilerLog += (card.cardName + ' x' + amount + '. ')  # print card name
        self.spoilerLog += '\n\n'

    def randomizeChestCardItems(self, chestCardItemList, doChestCards, doHiddenCards, doKeyItems, doItemOption, itemID):
        liveLocationList = list(chestCardItemList)  # make copy of list
        itemLocationDict = dict()
        if doChestCards:
            self.optionLog += 'Randomized chest cards\n'
        else:  # remove chest cards from list
            for location in chestCardItemList:
                if location.originalType == 1:
                    liveLocationList.remove(location)
        if doHiddenCards:
            self.optionLog += 'Randomized hidden cards\n'
        else:  # remove hidden cards from list
            for location in chestCardItemList:
                if location.originalType == 2:
                    liveLocationList.remove(location)
        if doKeyItems:
            usableLocationList = list(liveLocationList)
            if not doItemOption:  # do not allow hidden cards to be items
                for location in liveLocationList:
                    if location.originalType == 2:
                        usableLocationList.remove(location)
            itemLocationDict = self.randomizeKeyItems(usableLocationList, itemID)
        else:  # remove key items from list
            for location in chestCardItemList:
                if location.originalType == 3 or location.originalType == 4:
                    liveLocationList.remove(location)
        # build output dict and log
        for location in liveLocationList:
            if location.address in itemLocationDict.keys():  # item goes there
                item = itemLocationDict[location.address]
                self.buildItemOutput(location, item)
            else:  # put card there
                card = self.getRandomCard()
                self.buildCardOutput(location, card)
        self.spoilerLog += '\n'

    def randomizeKeyItems(self, liveLocationList, itemID):
        self.optionLog += 'Randomized key items\n'
        self.fixForItems()
        IP = itemPlacer.ItemPlacer(liveLocationList, itemID)
        goodItems = False
        while not goodItems:  # keep going until good item locations
            goodItems = IP.randomizeItemLocations()
        itemLocationDict = IP.getItemLocationDict()
        return itemLocationDict

    def buildItemOutput(self, location, item):
        itemBytes = item.itemID
        if location.originalType == 1 or location.originalType == 2:  # originally chest or hidden card location
            # append item-get to itemID
            itemBytes += self.itemGetByte
        self.outputDict[location.address] = itemBytes
        self.spoilerLog += (
                    location.levelName + ' ' + location.description + ' has ' + item.itemName + ' [!]' + '\n')  # (Level name) (location) has (item name)

    def buildCardOutput(self, location, card):
        cardBytes = card.interactID
        if location.originalType == 3:  # originally item location
            # append card-get to interactID
            cardBytes += self.cardGetByte
        if location.originalType == 4:  # originally shayel key or wyht key
            self.outputDict[location.typeAddress] = self.cardGetByte
        self.outputDict[location.address] = cardBytes  # pair up location and card interact ID
        self.spoilerLog += (
                location.levelName + ' ' + location.description + ' has ' + card.cardName + '\n')  # (Level name) (location) has (card name)

    def randomizeWarriorWyhtCards(self, warriorWyhtList):
        self.spoilerLog += 'Warrior of Wyht cards:\n'
        for address in warriorWyhtList:
            card = self.getRandomCard()
            self.outputDict[address] = card.cardID
            self.spoilerLog += card.cardName + '. '  # print card name
        self.spoilerLog += '\n\n'

    def randomizeLevelBonusCards(self, levelBonusList):
        self.optionLog += 'Randomized level bonus cards\n'
        for levelBonusSlot in levelBonusList:  # cardSlot: [memory address,...]
            for address in levelBonusSlot.adresses:
                card = self.getRandomCard()
                self.outputDict[address] = card.cardID

    def randomizeShopCards(self, shopCardList):
        self.optionLog += 'Randomized shop cards\n'
        self.spoilerLog += 'Shop cards:\n'
        n = 0
        for address in shopCardList:
            n += 1
            card = self.getRandomCard()
            self.outputDict[address] = card.cardID
            self.spoilerLog += card.cardName + '. '  # print card name
            if n % 10 == 0:  # every tenth card start new line
                self.spoilerLog += '\n'
        self.spoilerLog += '\n'

    def randomizeFairyCards(self, fairyCardList):
        self.optionLog += 'Randomized red fairy rewards\n'
        self.spoilerLog += 'Red fairy rewards:\n'
        for address in fairyCardList:
            card = self.getRandomCard()
            self.outputDict[address] = card.cardID
            self.spoilerLog += card.cardName + '. '  # print card name

    def randomizeAttributes(self, enemyAttributeList):
        self.optionLog += 'Randomized enemy attributes\n'
        for address in enemyAttributeList:  # member: memory address
            attributeIndex = random.randint(0, len(self.attributeCodes) - 1)  # choose random attribute
            self.outputDict[address] = self.attributeCodes[attributeIndex]

    def removeEscapeBattle(self):
        self.optionLog += 'Can\'t escape battles\n'
        self.outputDict[self.escapeBattleAddress] = self.nopCode

    def deactivateDeckPoints(self, deckPointsList):
        self.optionLog += 'Deactivated deck points\n'
        for address in deckPointsList:
            self.outputDict[address] = self.zeroBytes

    def makeLK2CardChanges(self, lk2CardChangeList):
        self.optionLog += 'LKII card changes\n'
        for replacement in lk2CardChangeList:
            self.outputDict[replacement.address] = replacement.newValue

    def makeLK2EnemyChanges(self, lk2EnemyChangeList):
        self.optionLog += 'LKII enemy changes\n'
        for replacement in lk2EnemyChangeList:
            self.outputDict[replacement.address] = replacement.newValue

    def fixForItems(self):
        itemFixDict = {int(b'8BDF4', 16): self.nopCode,  # remove items load out
                       int(b'8BE20', 16): self.nopCode,  # remove items load in
                       int(b'89A40', 16): self.nopCode,  # remove candles
                       int(b'89AA4', 16): self.nopCode,  # remove sheet music
                       int(b'89AF0', 16): self.nopCode,  # remove shayel key
                       int(b'89B50', 16): self.nopCode,  # remove gems
                       int(b'89BA0', 16): self.nopCode,  # remove stone of darkness
                       int(b'89BE8', 16): self.nopCode,  # remove wyht key
                       int(b'89C60', 16): self.nopCode,  # remove stone of cleansing
                       int(b'89CAC', 16): self.nopCode,  # remove necklace of pharaoh
                       int(b'C8B44', 16): self.nopCode,  # close level after complete
                       int(b'1CB0B181', 16): self.zeroBytes,  # interact rohbach tree 1
                       int(b'1CB0BF01', 16): self.zeroBytes,  # interact rohbach tree 2
                       int(b'1CB0D0C1', 16): self.zeroBytes}  # interact rohbach tree 3
        self.outputDict.update(itemFixDict)

    def getRandomCard(self):
        index = random.randint(0, len(self.cardList) - 1)  # choose random index to pull from cardIDs
        return self.cardList[index]

    def setCardsList(self, cardData):
        self.cardList = cardData

    def getRandomizerOutput(self):
        return self.outputDict, self.optionLog, self.spoilerLog  # return tuple
