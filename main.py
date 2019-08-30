import fileLoad
import gui
import randomizer
import fileOutput
import tkinter as tk
import tkinter.messagebox as messagebox


class Mediator:
    # constants
    versionName = 'LK Randomizer v0.6'

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

    def startRandomizer(self, widgetVals):
        try:
            if not self.loader.isGoodISO(widgetVals['fileInput']):  # test for good .iso Path
                raise IOError
        except IOError:
            self.gui.showISOErrorMessage()
        else:
            randInstance = randomizer.Randomizer(widgetVals['seedInput'])
            randInstance.setCardsList(self.loader.cardList)  # pass card list to randomizer
            if widgetVals['startingDeckChecked']:
                randInstance.randomizeStartingDeck(self.loader.startingDeckList)
            if widgetVals['chestCardsChecked'] or widgetVals['hiddenCardsChecked'] or widgetVals['keyItemsChecked']:
                randInstance.randomizeChestCardItems(self.loader.chestCardItemList, widgetVals['chestCardsChecked'], widgetVals['hiddenCardsChecked'], widgetVals['keyItemsChecked'], widgetVals['itemOption'], self.loader.itemList)
                randInstance.randomizeWarriorWyhtCards(self.loader.warriorWyhtList)
            if widgetVals['levelBonusCardsChecked']:
                randInstance.randomizeLevelBonusCards(self.loader.levelBonusList)
            if widgetVals['shopCardsChecked']:
                randInstance.randomizeShopCards(self.loader.shopCardList)
            if widgetVals['fairyCardsChecked']:
                randInstance.randomizeFairyCards(self.loader.fairyCardList)
            if widgetVals['enemyAttributesChecked']:
                randInstance.randomizeAttributes(self.loader.enemyAttributeList)
            if widgetVals['escapeBattleChecked']:
                randInstance.removeEscapeBattle()
            if widgetVals['deckPointChecked']:
                randInstance.deactivateDeckPoints(self.loader.deckPointList)
            if widgetVals['lk2CardChecked']:
                randInstance.makeLK2CardChanges(self.loader.lk2CardChangeList)
            if widgetVals['lk2EnemyChecked']:
                randInstance.makeLK2EnemyChanges(self.loader.lk2EnemyChangeList)
            randOutputTup = randInstance.getRandomizerOutput()
            self.fileOutput(widgetVals['fileInput'], widgetVals['seedInput'], widgetVals['genIsoSelected'], widgetVals['includeSpoilersSelected'], randOutputTup)
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
