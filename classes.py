class Card:
    # rarity 1: common, 2: uncommon, 3: rare, 4: one-of-a-kind
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
    # originalType 1: chest card, 2: hidden card, 3: item chest, 4: item reward
    def __init__(self, address, originalType, area, levelName, description, typeAddress=None):
        self.address = address
        self.originalType = originalType
        self.area = area
        self.levelName = levelName
        self.description = description
        self.typeAddress = typeAddress


class Summon:
    # attackType 04: medium, 05: heavy
    def __init__(self, address, attackType):
        self.address = address
        self.attackType = attackType
