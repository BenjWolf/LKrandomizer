import fileLoad
import gui
import randomizer
import fileOutput
import tkinter as tk


class Mediator:

    def __init__(self):
        self.loader = fileLoad.FileLoad()
        root = tk.Tk()  # root to contain GUI
        savedFilePath = self.loader.loadSavedFilePath()  # user's file path for ISO
        self.gui = gui.GUI(self, root, savedFilePath)
        root.mainloop()  # start GUI

    def startRandomizer(self, widgetVals):
        try:
            if not self.loader.isGoodISO(widgetVals['fileInput']):  # test for good .iso Path
                raise IOError
        except IOError:
            self.gui.showISOErrorMessage()
        else:
            randInstance = randomizer.Randomizer(widgetVals['seedInput'])
            randInstance.setCardsList(self.loader.getCardList())  # pass card list to randomizer
            if widgetVals['startingDeckChecked']:
                randInstance.randomizeStartingDeck(self.loader.getStartingDeckList())
            if widgetVals['chestCardsChecked'] or widgetVals['hiddenCardsChecked']:
                randInstance.randomizeChestCardItems(self.loader.getchestCardItemList(), widgetVals['chestCardsChecked'], widgetVals['hiddenCardsChecked'])
            if widgetVals['levelBonusCardsChecked']:
                randInstance.randomizeLevelBonusCards(self.loader.getLevelBonusList())
            if widgetVals['shopCardsChecked']:
                randInstance.randomizeShopCards(self.loader.getShopCardList())
            if widgetVals['fairyCardsChecked']:
                randInstance.randomizeFairyCards(self.loader.getFairyCardList())
            if widgetVals['enemyAttributesChecked']:
                randInstance.randomizeAttributes(self.loader.getEnemyAttributeList())
            if widgetVals['escapeBattleChecked']:
                randInstance.removeEscapeBattle()
            if widgetVals['deckPointChecked']:
                randInstance.deactivateDeckPoints(self.loader.getDeckPointList())
            if widgetVals['summonCardChecked']:
                randInstance.removeSummonAnimations(self.loader.getSummonList())
            randOutputTup = randInstance.getRandomizerOutput()
            self.fileOutput(widgetVals['fileInput'], widgetVals['writeOptionSelected'], widgetVals['seedInput'], randOutputTup)
            self.gui.showDoneMessage()

    def fileOutput(self, isoPath, writeOption, seed, randOutputTup):  # randOutputTup (randOutput dict, optionLog string, randLog string)
        outputInstance = fileOutput.FileOutput()
        if writeOption == 1 or writeOption == 2:
            outputInstance.copyISO(isoPath, seed)
            outputInstance.changePlayerNameToSeed(seed)
            outputInstance.writeToISO(randOutputTup[0])
        if writeOption == 1 or writeOption == 3:
            outputInstance.writeToLog(seed, randOutputTup[1], randOutputTup[2])
        outputInstance.saveFilePath(isoPath)


if __name__ == '__main__':
    Mediator()
