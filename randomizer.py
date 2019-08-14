import random
import itemPlacer


class Randomizer:
    escapeBattleAddress = int(b'24A08', 16)
    attributeCodes = [b'\x00', b'\x01', b'\x02', b'\x03', b'\x00', b'\x01', b'\x02', b'\x03', b'\x04']  # doubled elemental attributes
    zeroBytes = bytes(b'\x00\x00')
    cardGetByte = b'\x66'
    itemGetByte = b'\x65'
    heavyWeaponBytes = bytes(b'\x05')  # todo assign this in data file
    nopCode = bytes(b'\x60\x00\x00\x00')

    def __init__(self, seedVal):
        self.seedVal = seedVal
        random.seed(a=self.seedVal)  # seed the random module
        self.cardList = list()  # member: [cardID, get-card ID, card name]
        self.outputDict = dict()  # key: address val: randomized value
        self.optionLog = 'Options:\n'
        self.spoilerLog = str()

    def randomizeStartingDeck(self, startingDeckList):
        self.optionLog += 'Randomized starting deck\n'
        self.spoilerLog += 'Starting Deck: '
        for cardSlot in startingDeckList:  # cardSlot: [memory address, memory address,...]
            card = self.getRandomCard()
            for address in cardSlot:
                self.outputDict[address] = card[0]
            amount = str((len(cardSlot) - 1))
            self.spoilerLog += (card[2] + ' x' + amount + '. ')  # print card name
        self.spoilerLog += '\n\n'

    def randomizeChestCardItems(self, chestCardItemList, doChestCards, doHiddenCards, doKeyItems, itemID):
        locationList = list(chestCardItemList)  # make copy of list
        itemLocationDict = dict()
        if doChestCards:
            self.optionLog += 'Randomized chest cards\n'
        else:  # remove chest cards from list
            for member in chestCardItemList:
                if member[1] == 1:
                    locationList.remove(member)
        if doHiddenCards:
            self.optionLog += 'Randomized hidden cards\n'
        else:  # remove hidden cards from list
            for member in chestCardItemList:
                if member[1] == 2:
                    locationList.remove(member)
        if doKeyItems:
            self.optionLog += 'Randomized key items\n'
            self.fixForItems()
            IP = itemPlacer.ItemPlacer(locationList, itemID)
            goodItems = False
            while not goodItems:  # keep going until good item locations
                goodItems = IP.randomizeItemLocations()
            itemLocationDict = IP.getItemLocationDict()
        else:  # remove key items from list
            for member in chestCardItemList:
                if member[1] == 3:
                    locationList.remove(member)
        # build output dict and log
        for location in locationList:
            if location[0] in itemLocationDict.keys():  # item goes there
                item = itemLocationDict[location[0]]
                if location[1] == 1 or location[1] == 2:  # originally chest or hidden card location
                    # append item-get to itemID
                    item[0] = item[0] + self.itemGetByte
                self.outputDict[location[0]] = item[0]
                self.spoilerLog += (location[3] + ' ' + location[4] + ' has ' + item[1] + ' [!]' + '\n')  # (Level name) (location) has (item name)
            else:  # put card there
                card = self.getRandomCard()
                if location[1] == 3:  # originally item location
                    # append card-get to cardID
                    card[1] = card[1] + self.cardGetByte
                self.outputDict[location[0]] = card[1]  # pair up location and get-card ID
                self.spoilerLog += (location[3] + ' ' + location[4] + ' has ' + card[2] + '\n')  # (Level name) (location) has (card name)
        self.spoilerLog += '\n'

    def randomizeLevelBonusCards(self, levelBonusList):
        self.optionLog += 'Randomized level bonus cards\n'
        for cardSlot in levelBonusList:  # cardSlot: [memory address,...]
            for address in cardSlot:
                card = self.getRandomCard()
                self.outputDict[address] = card[0]

    def randomizeShopCards(self, shopCardList):
        self.optionLog += 'Randomized shop cards\n'
        self.spoilerLog += 'Shop cards:\n'
        n = 0
        for address in shopCardList:
            n += 1
            card = self.getRandomCard()
            self.outputDict[address] = card[0]
            self.spoilerLog += card[2] + '. '  # print card name
            if n % 10 == 0:  # every tenth card start new line
                self.spoilerLog += '\n'
        self.spoilerLog += '\n'

    def randomizeFairyCards(self, fairyCardList):
        self.optionLog += 'Randomized red fairy rewards\n'
        self.spoilerLog += 'Red fairy rewards:\n'
        for address in fairyCardList:
            card = self.getRandomCard()
            self.outputDict[address] = card[0]
            self.spoilerLog += card[2] + '. '  # print card name

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

    def removeSummonAnimations(self, summonList):
        self.optionLog += 'Removed summon animations\n'
        for card in summonList:  # member: memory address
            self.outputDict[card[0]] = card[1]

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
                       int(b'1CB0B181', 16): self.zeroBytes,  # rohbach tree 1
                       int(b'1CB0BF01', 16): self.zeroBytes,  # rohbach tree 2
                       int(b'1CB0D0C1', 16): self.zeroBytes}  # rohbach tree 3
        self.outputDict.update(itemFixDict)

    def getRandomCard(self):
        index = random.randint(0, len(self.cardList) - 1)  # choose random index to pull from cardIDs
        return self.cardList[index]

    def setCardsList(self, cardData):
        self.cardList = cardData

    def getRandomizerOutput(self):
        return self.outputDict, self.optionLog, self.spoilerLog  # return tuple
