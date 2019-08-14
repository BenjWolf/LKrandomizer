import random

class ItemPlacer:

    def __init__(self, locationList, itemIDs):
        self.locationList = list(locationList) # copy of chest card item .csv / when items get placed in a location they are removed from here
        self.itemList = list(itemIDs)  # member [item ID, item name] / start with all items, removes until empty
        self.allItems = list(itemIDs)
        self.inventoryDict = dict()  # key: item name. value: bool (true when in inventory)
        self.itemLocationDict = dict()  # items placed in location key: address from locationList, value: itemID
        self.areaGraph = dict()  # area connections
        self.itemsInArea = dict()  # what items are in an area. key: area num. value: item name
        self.setDicts()

    def startInventory(self):
        # start with all items
        for item in self.allItems:
            self.inventoryDict[item[1]] = True

    def setInventory(self):
        # start with no items
        for slot in self.inventoryDict:
            self.inventoryDict[slot] = False
        # add items that haven't been placed yet
        for item in self.itemList:
            self.inventoryDict[item[1]] = True

    def setDicts(self):
        self.areaGraph = {1: [2],
                          2: [3, 4],
                          4: [5, 6],
                          6: [7, 8],
                          8: [9, 10]}
        self.itemsInArea = {1: list(),
                            2: list(),
                            3: list(),
                            4: list(),
                            5: list(),
                            6: list(),
                            7: list(),
                            8: list(),
                            9: list(),
                            10: list()}

    def randomizeItemLocations(self):
        self.startInventory()
        # add set item list
        while len(self.itemList) > 0:
            accessibleAreaList = list()
            accessibleAreaList.append(1)
            # remove item from inventory
            removedItem = self.removeItemFromInventory()
            self.setInventory()
            # traverse map
            for area in accessibleAreaList:
                # get items in area
                for item in self.itemsInArea[area]:
                    self.inventoryDict[item] = True
                # add acessible areas to list
                if area in self.areaGraph:
                    connectedArea = self.areaGraph[area]
                    # check if we can get to another area
                    for conArea in connectedArea:
                        if self.haveAreaRequirment(conArea):
                            accessibleAreaList.append(conArea)
            # place item somewhere accessible
            if not self.placeItem(removedItem, accessibleAreaList):
                return False  # no place to put item
        return True

    def haveAreaRequirment(self, area):
        # relative requirements to get to an area
        areaItemReq = {2: self.inventoryDict['Shayel Key'],
                       3: self.inventoryDict['Fruit of Mandragora'] and self.inventoryDict['Bark of Treant'] and self.inventoryDict['Man Trap Leaf'],
                       4: self.inventoryDict['Key of Castle Wyht'],
                       5: self.inventoryDict['Old Sheet Music'],
                       6: self.inventoryDict['Red Candle'] and self.inventoryDict['Blue Candle'] and self.inventoryDict['Yellow Candle'] and self.inventoryDict['Green Candle'],
                       7: self.inventoryDict['Fruit of Mandragora'] and self.inventoryDict['Bark of Treant'] and self.inventoryDict['Man Trap Leaf'],
                       8: self.inventoryDict['Black Gem'] and self.inventoryDict['White Gem'],
                       9: self.inventoryDict['Necklace of the Pharaoh'],
                       10: self.inventoryDict['Stone of Darkness']}
        return areaItemReq[area]

    def removeItemFromInventory(self):
        index = random.randint(0, len(self.itemList) - 1)
        item = self.itemList[index]
        self.itemList.remove(item)
        return item

    def placeItem(self, item, accessibleAreaList):
        availableLocations = self.getAvailableLocations(accessibleAreaList)
        if len(availableLocations) > 0:
            index = random.randint(0, len(availableLocations) - 1)
            location = availableLocations[index]
            # add item to dict
            self.itemLocationDict[location[0]] = item
            # remove location from list
            self.locationList.remove(location)
            # add item to area
            area = location[2]
            self.itemsInArea[area].append(item[1])
            return True
        else:  # no available locations
            return False

    def getAvailableLocations(self, accessibleAreaList):
        availableLocationsList = list(self.locationList)
        # remove inacessible locations
        for location in self.locationList:
            if location[2] not in accessibleAreaList:
                availableLocationsList.remove(location)
        return availableLocationsList

    def getItemLocationDict(self):
        return self.itemLocationDict
