import fileLoad
import gui
import randomizer
import balancedRandomizer
import fileOutput
import tkinter as tk
import tkinter.messagebox as messagebox


class Mediator:
    # constants
    versionName = 'LK Randomizer v0.7'

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
            if widgetVars.randomStyle.get() == 1:  # full random
                randInstance = randomizer.Randomizer(widgetVars.seedInput.get(), self.loader.cardList, self.loader.levelDict)
            else:  # balanced random
                randInstance = balancedRandomizer.BalancedRandomizer(widgetVars.seedInput.get(), self.loader.cardList, self.loader.levelDict)
            if widgetVars.startingDeckChecked.get():
                randInstance.randomizeStartingDeck(self.loader.startingDeckFullRandomList, self.loader.startingDeckBalancedList, self.loader.startingInventoryASMDict)
            if widgetVars.chestCardsChecked.get() or widgetVars.hiddenCardsChecked.get() or widgetVars.keyItemsChecked.get():
                randInstance.randomizeChestCardItems(self.loader.chestCardItemList, widgetVars.chestCardsChecked.get(), widgetVars.hiddenCardsChecked.get(), widgetVars.keyItemsChecked.get(), widgetVars.itemHiddenCardChecked.get(), self.loader.itemList)
                randInstance.randomizeWarriorWyhtCards(self.loader.warriorWyhtList)
            if widgetVars.levelBonusCardsChecked.get():
                randInstance.randomizeLevelBonusCards(self.loader.levelBonusList)
            if widgetVars.shopCardsChecked.get():
                randInstance.randomizeShopCards(self.loader.shopCardList)
            if widgetVars.fairyCardsChecked.get():
                randInstance.randomizeFairyCards(self.loader.fairyCardList)
            if widgetVars.enemyAttributesChecked.get():
                randInstance.randomizeAttributes(self.loader.enemyAttributeList)
            if widgetVars.escapeBattleChecked.get():
                randInstance.removeEscapeBattle()
            if widgetVars.deckPointChecked.get():
                randInstance.deactivateDeckPoints(self.loader.deckPointList)
            if widgetVars.lk2CardChecked.get():
                randInstance.makeLK2CardChanges(self.loader.lk2CardChangeList)
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
