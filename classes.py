class Card:
    """
    cardID (byte): when receiving card in menus
    interactID (byte): when receiving card from interact
    cardName (str)
    rarity (int): 1: common, 2: uncommon, 3: rare, 4: one-of-a-kind
    """
    def __init__(self, cardID, interactID, cardName, rarity):
        self.cardID = cardID
        self.interactID = interactID
        self.cardName = cardName
        self.rarity = rarity


class Item:
    """
    itemID (byte)
    itemName (str)
    """
    def __init__(self, itemID, itemName):
        self.itemID = itemID
        self.itemName = itemName


class Location:
    """
    address (int16): iso offset of object to receive from interaction
    originalType (int): 1: chest card, 2: hidden card, 3: item chest, 4: item reward
    area (int): for key item logic
    levelName (str)
    description (str)
    originalInteractID (byte): value we are replacing
    typeAddress (int16)(optional): only used if interact address is not followed by type address in iso
    """
    def __init__(self, address, originalType, area, levelName, description, originalInteractID, typeAddress=None):
        self.address = address
        self.originalType = originalType
        self.area = area
        self.levelName = levelName
        self.description = description
        self.originalInteractID = originalInteractID
        self.typeAddress = typeAddress


class LevelBonusSlot:
    """
    A slot is made up of multiples of the same card. A slot may have 1 to 4 multiples.
    addresses (list of int16): iso offset of cards in slot
    originalCardID (byte): value we are replacing
    """
    def __init__(self, adresses, originalCardID):
        self.adresses = adresses
        self.originalCardID = originalCardID


class ReplaceBytes:
    """
    Data that needs to be replaced on .iso
    address (int16): iso offset of value to be replaced
    newValue (bytes): new value to write to .iso
    """
    def __init__(self, address, newValue):
        self.address = address
        self.newValue = newValue
