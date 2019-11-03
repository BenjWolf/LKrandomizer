import random


class ItemHintGen:
    lineLength = 27

    def __init__(self, levelDict, itemList, locationList, locationItemDict, npcAddressList):
        self.levelDict = levelDict
        self.itemList = itemList
        self.locationList = locationList
        self.locationItemDict = locationItemDict
        self.npcAddressList = npcAddressList
        self.hintDict = dict()

    def generateHints(self):
        for address in self.npcAddressList:
            index = random.randint(1, 3)
            if index == 1:
                hintString = self.generateHowManyItemsHint()
            elif index == 2:
                hintString = self.generateItemLevelHint(True)
            else:
                hintString = self.generateItemLevelHint(False)
            hintString = self.prepareHintString(hintString)
            self.hintDict[address] = hintString

    def generateHowManyItemsHint(self):
        # choose level from random
        levelIDs = list(self.levelDict.keys())
        index = random.randint(0, len(levelIDs) - 1)
        level = self.levelDict[levelIDs[index]]
        # determine how many items in level
        numItems = 0
        for location in self.locationList:
            if location.levelID == level.levelID:
                if location in self.locationItemDict:
                    numItems += 1
        if numItems == 0:
            returnString = 'They say there is nothing useful in ' + level.levelName + '.'
        elif numItems == 1:
            returnString = 'They say there is a useful item in ' + level.levelName + '.'
        else:
            returnString = 'They say there are ' + str(numItems) + ' useful items in ' + level.levelName + '.'
        return returnString

    def generateItemLevelHint(self, useLevelName):
        # choose item from random
        index = random.randint(0, len(self.itemList) - 1)
        item = self.itemList[index]
        # determine which level it is in
        locations = list(self.locationItemDict.keys())
        items = list(self.locationItemDict.values())
        location = locations[items.index(item)]
        level = self.levelDict[location.levelID]
        if useLevelName:
            returnString = 'They say the ' + item.itemName + ' is in ' + level.levelName + '.'
        else:
            index = random.randint(0, len(level.hints) - 1)
            returnString = 'They say the ' + item.itemName + level.hints[index] + '.'
        return returnString

    def prepareHintString(self, hintString):
        index = 0
        newString = ''
        moreString = True
        while moreString:
            # take 27 chars
            workingString = hintString[index:index + self.lineLength]
            if len(workingString) == self.lineLength:
                # find space
                spaceIndex = workingString.rfind(' ')
                workingString = workingString[0:spaceIndex] + '\r\n'
                index += spaceIndex + 1
            else:  # end of string
                moreString = False
            newString += workingString
        # append null char
        newString += '\u0000'
        return newString.encode('utf-8')

    def getHintDict(self):
        return self.hintDict

