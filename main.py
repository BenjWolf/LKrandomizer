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

    def startRandomizer(self, isoPath, startingDeckChecked, chestChecked, hiddenChecked, levelBonusChecked, enemyAttributes, deckPointChecked, writeOption, seed):
        try:
            if not self.loader.isGoodISO(isoPath):
                raise IOError
        except IOError:
            self.gui.showISOErrorMessage()
        else:
            randInstance = randomizer.Randomizer(seed)
            if startingDeckChecked or chestChecked or hiddenChecked or levelBonusChecked:
                randInstance.setCardsList(self.loader.loadCardData())  # pass card list to randomizer
            if startingDeckChecked:
                randInstance.setStartingDeckList(self.loader.loadStartingDeck())
            if chestChecked:
                randInstance.setChestList(self.loader.loadChests())
            if hiddenChecked:
                randInstance.setHiddenList(self.loader.loadHiddenCards())
            if levelBonusChecked:
                randInstance.setLevelBonusList(self.loader.loadLevelBonusCards())
            if enemyAttributes:
                randInstance.setEnemyAttributeList(self.loader.loadEnemyAttributes())
            if deckPointChecked:
                randInstance.setDeckPointsList(self.loader.loadDeckPoints())
            randOutputTup = randInstance.start()  # do randomization and store output in tuple
            self.fileOutput(isoPath, writeOption, seed, randOutputTup)
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
