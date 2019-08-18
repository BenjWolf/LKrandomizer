import fileLoad
import gui
import randomizer
import fileOutput
import tkinter as tk


class Mediator:
    # constants
    versionName = 'LK Randomizer v0.5'

    def __init__(self):
        self.loader = fileLoad.FileLoad()
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
                randInstance.randomizeChestCardItems(self.loader.chestCardItemList, widgetVals['chestCardsChecked'], widgetVals['hiddenCardsChecked'], widgetVals['keyItemsChecked'], self.loader.itemList)
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
            if widgetVals['summonCardChecked']:
                randInstance.removeSummonAnimations(self.loader.summonList)
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
