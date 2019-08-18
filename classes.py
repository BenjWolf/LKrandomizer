class Card:
    def __init__(self, cardID, interactID, cardName, rarity):
        self.cardID = cardID
        self.interactID = interactID
        self.cardName = cardName
        self.rarity = rarity


class Item:
    def __init__(self, itemID, itemName):
        self.itemID = itemID
        self.itemName = itemName


class Location:
    def __init__(self, address, originalType, area, levelName, description):
        self.address = address
        self.originalType = originalType
        self.area = area
        self.levelName = levelName
        self.description = description


class Summon:
    def __init__(self, address, attackType):
        self.address = address
        self.attackType = attackType
