import fileLoad
import gui
import randomizer
import balancedRandomizer
import fileOutput
import tkinter as tk
import tkinter.messagebox as messagebox


class Mediator:
    # constants
    versionName = 'LK Randomizer v0.8'

    def __init__(self):
        try:
            self.loader = fileLoad.FileLoad()
        except IOError:
            messagebox.showerror('Error', 'Missing data files')
        else:
            root = tk.Tk()  # root to contain GUI
            savedFilePath = self.loader.loadSavedFilePath()  # user's file path for ISO
            self.gui = gui.GUI(self, root, savedFilePath, self.versionName)
            root.mainloop()  # start GUI

    def startRandomizer(self, widgetVars):
        try:
            if not self.loader.isGoodISO(widgetVars.fileInput.get()):  # test for good .iso Path
                raise IOError
        except IOError:
            self.gui.showISOErrorMessage()
        else:
            # make instance of randomizer
            if widgetVars.randomStyle.get() == 1:  # full random
                randInstance = randomizer.Randomizer(widgetVars.seedInput.get(), self.loader.cardList, self.loader.levelDict, self.loader.itemList, self.loader.locationList, fairPlayOnly=widgetVars.fairPlay)
            else:  # balanced random
                randInstance = balancedRandomizer.BalancedRandomizer(widgetVars.seedInput.get(), self.loader.cardList, self.loader.levelDict, self.loader.itemList, self.loader.locationList, fairPlayOnly=widgetVars.fairPlay)
            # starting deck
            if widgetVars.startingDeckChecked.get():
                randInstance.randomizeStartingDeck(self.loader.startingDeckFullRandomList, self.loader.startingDeckBalancedList, self.loader.startingInventoryASMDict)
            # chest cards, hidden cards, and items
            if widgetVars.chestCardsChecked.get():
                randInstance.doChestCards()
            else:
                randInstance.removeChests()
            if widgetVars.hiddenCardsChecked.get():
                randInstance.doHiddenCards()
            else:
                randInstance.removeHiddenCards()
            if widgetVars.keyItemsChecked.get():
                randInstance.doKeyItems()
                if widgetVars.itemHintsChecked.get():
                    randInstance.doItemHints(self.loader.npcAddressList)
            else:
                randInstance.removeKeyItems()
            if widgetVars.chestCardsChecked.get() or widgetVars.hiddenCardsChecked.get() or widgetVars.keyItemsChecked.get():
                randInstance.randomizeLocations()
                randInstance.randomizeWarriorWyhtCards(self.loader.warriorWyhtList)
            # level bonus cards
            if widgetVars.levelBonusCardsChecked.get():
                randInstance.randomizeLevelBonusCards(self.loader.levelBonusList)
            # shop cards
            if widgetVars.shopCardsChecked.get():
                randInstance.randomizeShopCards(self.loader.shopCardList)
            # fairy cards
            if widgetVars.fairyCardsChecked.get():
                randInstance.randomizeFairyCards(self.loader.fairyCardList)
            # enemy attributes
            if widgetVars.enemyAttributesChecked.get():
                randInstance.randomizeAttributes(self.loader.enemyAttributeList)
            # escape battle
            if widgetVars.escapeBattleChecked.get():
                randInstance.removeEscapeBattle()
            # deck point
            if widgetVars.deckPointChecked.get():
                randInstance.deactivateDeckPoints(self.loader.deckPointList)
            # lk2 card
            if widgetVars.lk2CardChecked.get():
                randInstance.makeLK2CardChanges(self.loader.lk2CardChangeList)
            # lk2 enemy
            if widgetVars.lk2EnemyChecked.get():
                randInstance.makeLK2EnemyChanges(self.loader.lk2EnemyChangeList)
            randOutputTup = randInstance.getRandomizerOutput()
            self.fileOutput(widgetVars.fileInput.get(), widgetVars.seedInput.get(), widgetVars.genIsoSelected.get(), widgetVars.includeSpoilersSelected.get(), randOutputTup)
            self.gui.showDoneMessage()

    def fileOutput(self, isoPath, seed, genIso, includeSpoilers, randOutputTup):  # randOutputTup (randOutput dict, optionLog string, randLog string)
        outputInstance = fileOutput.FileOutput()
        if genIso:
            outputInstance.copyISO(isoPath, seed)
            outputInstance.changePlayerNameToSeed(seed)
            outputInstance.writeToISO(randOutputTup[0])
        if includeSpoilers:
            spoilers = randOutputTup[2]
        else:
            spoilers = 'No spoilers'
        outputInstance.writeToLog(self.versionName, seed, randOutputTup[1], spoilers)
        outputInstance.saveFilePath(isoPath)


if __name__ == '__main__':
    Mediator()
