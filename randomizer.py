import random
import itemPlacer
import itemHintGen


class Randomizer:
    escapeBattleAddress = int(b'24A08', 16)
    attributeCodes = [b'\x00', b'\x01', b'\x02', b'\x03', b'\x00', b'\x01', b'\x02', b'\x03', b'\x04']  # doubled elemental attributes
    zeroBytes = bytes(b'\x00\x00')
    cardGetByte = b'\x66'
    itemGetByte = b'\x65'
    nopCode = bytes(b'\x60\x00\x00\x00')

    def __init__(self, seedVal, cardList, levelDict, itemList, locationList):
        random.seed(a=seedVal)  # seed the random module
        self.cardList = cardList  # member: card object
        self.levelDict = levelDict  # member: level object
        self.itemList = itemList
        self.staticLocationList = locationList
        self.liveLocationList = list(locationList)  # start with every location to be randomized, remove locations not randomized
        self.IP = None  # item placer object
        self.outputDict = dict()  # key: address val: new value to write
        self.optionLog = 'Options:\n'
        self.writeRandomizationStyleToLog()
        self.spoilerLog = str()

    def writeRandomizationStyleToLog(self):
        self.optionLog += 'Full randomization style\n'

    def randomizeStartingDeck(self, fullRandomDeckList, balancedDeckList, asmDict):
        self.outputDict.update(asmDict)  # make asm changes first
        self.optionLog += 'Randomized starting deck\n'
        self.spoilerLog += 'Starting Deck: '
        for cardSlot in fullRandomDeckList:  # cardSlot: [memory address, memory address,...]
            card = self.getRandomCard()
            self.outputDict[cardSlot[0]] = card.cardID
            self.outputDict[cardSlot[1]] = card.cardID
            self.spoilerLog += (card.cardName + '. ')  # print card name
        self.spoilerLog += '\n\n'

    def doChestCards(self):
        self.optionLog += 'Randomized chest cards\n'

    def doHiddenCards(self):
        self.optionLog += 'Randomized hidden cards\n'

    def doKeyItems(self):
        self.optionLog += 'Randomized key items\n'
        self.fixForItems()
        usableLocationList = list(self.liveLocationList)
        for location in self.liveLocationList:
            if location.originalType == 2:
                # remove hidden card locations
                usableLocationList.remove(location)
        self.IP = itemPlacer.ItemPlacer(usableLocationList, self.itemList)
        goodItems = False
        while not goodItems:  # keep going until good item locations
            goodItems = self.IP.randomizeItemLocations()

    def doItemHints(self, npcAddressList):
        self.optionLog += 'NPCs give hints\n'
        IHG = itemHintGen.ItemHintGen(self.levelDict, self.itemList, self.staticLocationList, self.IP.getLocationItemDict(), npcAddressList)
        IHG.generateHints()
        self.outputDict.update(IHG.getHintDict())

    def removeChests(self):
        for location in self.staticLocationList:
            if location.originalType == 1:
                self.liveLocationList.remove(location)

    def removeHiddenCards(self):
        for location in self.staticLocationList:
            if location.originalType == 2:
                self.liveLocationList.remove(location)

    def removeKeyItems(self):
        for location in self.staticLocationList:
            if location.originalType == 3 or location.originalType == 4:
                self.liveLocationList.remove(location)

    def randomizeLocations(self):
        if self.IP is not None:  # items were placed
            locationItemDict = self.IP.getLocationItemDict()
        else:
            locationItemDict = dict()
        # build output dict and log
        for location in self.liveLocationList:
            if location in locationItemDict.keys():  # item goes there
                item = locationItemDict[location]
                self.buildItemOutput(location, item)
            else:  # put card there
                card = self.getRandomCard()
                self.buildCardOutput(location, card)
        self.spoilerLog += '\n'

    def buildItemOutput(self, location, item):
        itemBytes = item.itemID
        if location.originalType == 1 or location.originalType == 2:  # originally chest or hidden card location
            # append item-get to itemID
            itemBytes += self.itemGetByte
        self.outputDict[location.address] = itemBytes
        levelName = self.levelDict[location.levelID].levelName
        self.spoilerLog += (
                    levelName + ' - ' + location.description + ' has ' + item.itemName + ' [!]' + '\n')  # (Level name) (location) has (item name)

    def buildCardOutput(self, location, card):
        cardBytes = card.interactID
        if location.originalType == 3:  # originally item location
            # append card-get to interactID
            cardBytes += self.cardGetByte
        if location.originalType == 4:  # originally shayel key or wyht key
            self.outputDict[location.typeAddress] = self.cardGetByte
        self.outputDict[location.address] = cardBytes  # pair up location and card interact ID
        levelName = self.levelDict[location.levelID].levelName
        self.spoilerLog += (
                levelName + ' - ' + location.description + ' has ' + card.cardName + '\n')  # (Level name) (location) has (card name)

    def randomizeWarriorWyhtCards(self, warriorWyhtList):
        self.spoilerLog += 'Warrior of Wyht cards:\n'
        for warrior in warriorWyhtList:
            card = self.getRandomCard()
            self.outputDict[warrior.cardAddress] = card.cardID
            self.spoilerLog += card.cardName + '. '  # print card name
            self.prepareWarriorDialogue(warrior, card)
        self.spoilerLog += '\n\n'

    def prepareWarriorDialogue(self, warrior, card):
        dialogueString = 'The dying warrior gives you \r\na ' + card.cardName + ' card.\u0000'
        dialogueString = dialogueString.encode('utf-8')
        self.outputDict[warrior.dialogueAddress] = dialogueString

    def randomizeLevelBonusCards(self, levelBonusList):
        self.optionLog += 'Randomized level bonus cards\n'
        for levelBonusSlot in levelBonusList:  # cardSlot: [memory address,...]
            for address in levelBonusSlot.addressList:
                card = self.getRandomCard()
                self.outputDict[address] = card.cardID

    def randomizeShopCards(self, shopCardList):
        self.optionLog += 'Randomized shop cards\n'
        self.spoilerLog += 'Shop cards:\n'
        n = 0
        for shopCard in shopCardList:
            n += 1
            card = self.getRandomCard()
            self.outputDict[shopCard.address] = card.cardID
            self.spoilerLog += card.cardName + '. '  # print card name
            if n % 10 == 0:  # every tenth card start new line
                self.spoilerLog += '\n'
        self.spoilerLog += '\n'

    def randomizeFairyCards(self, fairyCardList):
        self.optionLog += 'Randomized red fairy rewards\n'
        self.spoilerLog += 'Red fairy rewards:\n'
        for fairyCard in fairyCardList:
            card = self.getRandomCard()
            self.outputDict[fairyCard.address] = card.cardID
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
            self.outputDict[replacement.address] = replacement.value

    def makeLK2EnemyChanges(self, lk2EnemyChangeList):
        self.optionLog += 'LKII enemy changes\n'
        for replacement in lk2EnemyChangeList:
            self.outputDict[replacement.address] = replacement.value

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
        card = self.cardList[index]
        return card

    def getRandomizerOutput(self):
        return self.outputDict, self.optionLog, self.spoilerLog  # return tuple

