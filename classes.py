import tkinter as tk


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
    levelID (int)
    description (str)
    originalInteractID (byte): value we are replacing
    typeAddress (int16)(optional): only used if interact address is not followed by type address in iso
    """
    def __init__(self, address, originalType, area, levelID, description, originalInteractID, typeAddress=None):
        self.address = address
        self.originalType = originalType
        self.area = area
        self.levelID = levelID
        self.description = description
        self.originalInteractID = originalInteractID
        self.typeAddress = typeAddress


class LevelBonusSlot:
    """
    A slot is made up of multiples of the same card. A slot may have 1 to 4 multiples.
    addresses (list of int16): iso offset of cards in slot
    originalCardID (byte): value we are replacing
    """
    def __init__(self, addressList, originalCardID):
        self.addressList = addressList
        self.originalCardID = originalCardID


class AddressValue:
    """
    Data pair representing .iso address and either a new or original value
    address (int16): iso offset of value to be replaced
    value (bytes): new value to write to .iso or the original value
    """
    def __init__(self, address, value):
        self.address = address
        self.value = value


class StartingDeckSlot:
    """
    A slot is made up of multiples of the same card. A slot may have 1 to 4 multiples.
    addressList (list of int16): iso offset of cards in slot to be replaced
    replaceCardList (list of byte): potential cardIDs to use in replacement
    """
    def __init__(self, addressList, replaceCardList):
        self.addressList = addressList
        self.replaceCardList = replaceCardList


class Level:
    """
    levelID (int)
    levelName (str)
    hints(list of str)
    """
    def __init__(self, levelID, levelName, hints):
        self.levelID = levelID
        self.levelName = levelName
        self.hints = hints


class WidgetVars:
    """
    Every tkinter Var object that needs to be passed from GUI to main
    """
    def __init__(self):
        self.fileInput = tk.StringVar()
        self.startingDeckChecked = tk.BooleanVar()
        self.chestCardsChecked = tk.BooleanVar()
        self.hiddenCardsChecked = tk.BooleanVar()
        self.levelBonusCardsChecked = tk.BooleanVar()
        self.shopCardsChecked = tk.BooleanVar()
        self.fairyCardsChecked = tk.BooleanVar()
        self.enemyAttributesChecked = tk.BooleanVar()
        self.keyItemsChecked = tk.BooleanVar()
        self.itemHintsChecked = tk.BooleanVar()
        self.itemHiddenCardChecked = tk.BooleanVar()
        self.escapeBattleChecked = tk.BooleanVar()
        self.deckPointChecked = tk.BooleanVar()
        self.lk2CardChecked = tk.BooleanVar()
        self.lk2EnemyChecked = tk.BooleanVar()
        self.randomStyle = tk.IntVar()
        self.genIsoSelected = tk.BooleanVar()
        self.includeSpoilersSelected = tk.BooleanVar()
        self.seedInput = tk.StringVar()