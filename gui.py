import seedGen
import tkinter as tk
import tkinter.filedialog as fdialog
import tkinter.messagebox as messagebox


class GUI:

    def __init__(self, mediator, masterWindow, savedFilePath):
        self.mediator = mediator
        self.masterWindow = masterWindow
        self.masterWindow.title('LK Randomizer')
        self.masterWindow.resizable('false', 'false')
        self.seedGenInstance = seedGen.SeedGenerator()
        self.filePath = savedFilePath
        self.fileInput = tk.StringVar()
        self.startingDeckChecked = tk.BooleanVar()
        self.chestCardsChecked = tk.BooleanVar()
        self.hiddenCardsChecked = tk.BooleanVar()
        self.levelBonusCardsChecked = tk.BooleanVar()
        self.enemyAttributesChecked = tk.BooleanVar()
        self.deckPointChecked = tk.BooleanVar()
        self.writeOptionSelected = tk.IntVar()
        self.seedInput = tk.StringVar()
        self.makeFileSelection()
        self.makeStartButton()
        self.makeRandomOptions()
        self.makeDifficultyOptions()
        self.makeGenerationOptions()

    def makeFileSelection(self):
        # top frame
        topFrame = tk.Frame(self.masterWindow, bd=10)
        topFrame.pack()

        # File selection
        self.fileInput.set(self.filePath)
        fileEntry = tk.Entry(topFrame, textvariable=self.fileInput, width=48)
        fileEntry.pack(side='left')

        fileButton = tk.Button(topFrame, text='Select .iso', command=lambda: self.selectISO(fileEntry))
        fileButton.pack(side='left')

    def makeRandomOptions(self):
        # leftmost frame
        randomOptionsFrame = tk.Frame(self.masterWindow, bd=14)
        randomOptionsFrame.pack(side='left', anchor='n')

        optionsLabel = tk.Label(randomOptionsFrame, text='Include random:')
        optionsLabel.pack(anchor='w')

        # Check buttons
        startingDeckButton = tk.Checkbutton(randomOptionsFrame, text='Starting Deck', variable=self.startingDeckChecked)
        startingDeckButton.select()
        startingDeckButton.pack(anchor='w')

        chestButton = tk.Checkbutton(randomOptionsFrame, text='Chest Cards', variable=self.chestCardsChecked)
        chestButton.select()
        chestButton.pack(anchor='w')

        hiddenCardsButton = tk.Checkbutton(randomOptionsFrame, text='Hidden Cards', variable=self.hiddenCardsChecked)
        hiddenCardsButton.select()
        hiddenCardsButton.pack(anchor='w')

        levelBonusCardsButton = tk.Checkbutton(randomOptionsFrame, text='\'Level Bonus\' Cards', variable=self.levelBonusCardsChecked)
        levelBonusCardsButton.select()
        levelBonusCardsButton.pack(anchor='w')

        enemyAttributeButton = tk.Checkbutton(randomOptionsFrame, text='Enemy Attributes', variable=self.enemyAttributesChecked)
        enemyAttributeButton.pack(anchor='w')

    def makeDifficultyOptions(self):
        # middle frame
        difficultyFrame = tk.Frame(self.masterWindow, bd=14)
        difficultyFrame.pack(side='left', anchor='n')

        optionsLabel = tk.Label(difficultyFrame, text='Difficulty:')
        optionsLabel.pack(anchor='w')

        # Check buttons
        deckPointButton = tk.Checkbutton(difficultyFrame, text='Deactivate deck points', variable=self.deckPointChecked)
        deckPointButton.pack(anchor='w')

    def makeGenerationOptions(self):
        # rightmost frame
        generationOptionsFrame = tk.Frame(self.masterWindow, bd=14)
        generationOptionsFrame.pack(side='left')

        # Radio buttons
        bothButton = tk.Radiobutton(generationOptionsFrame, text='Generate .iso + log', variable=self.writeOptionSelected, value=1)
        bothButton.select()
        bothButton.pack(anchor='w')

        isoButton = tk.Radiobutton(generationOptionsFrame, text='Generate .iso only', variable=self.writeOptionSelected, value=2)
        isoButton.pack(anchor='w')

        logButton = tk.Radiobutton(generationOptionsFrame, text='Generate log only', variable=self.writeOptionSelected, value=3)
        logButton.pack(anchor='w')

        seedFrame = tk.Frame(generationOptionsFrame)
        seedFrame.pack()

        # seed
        seedLabel = tk.Label(seedFrame, text='Seed: ')
        seedLabel.pack(side='left')

        self.setSeedInputRandom()
        seedEntry = tk.Entry(seedFrame, textvariable=self.seedInput, width=16)
        seedEntry.pack(side='left')

        newSeedButton = tk.Button(generationOptionsFrame, text='New Seed', command=lambda: self.setSeedInputRandom())
        newSeedButton.pack()

    def makeStartButton(self):
        # bottom frame
        bottomFrame = tk.Frame(self.masterWindow, bd=12)
        bottomFrame.pack(side='bottom')
        # start button
        randomizeButton = tk.Button(bottomFrame, text='Start Randomization', bg='#65c421', activebackground='yellow', command=lambda: self.randomizeButtonPressed(self.fileInput.get()))
        randomizeButton.pack()

    def selectISO(self, fileEntry):
        filename = fdialog.askopenfilename(initialdir='/', title='Select file', filetypes=(('ISO files', '*.iso'), ('all files', '*.*')))
        length = len(fileEntry.get())
        fileEntry.delete(0, length)  # clear text
        fileEntry.insert(0, filename)  # insert text to textbox

    def randomizeButtonPressed(self, isoPath):
        try:
            if not self.seedInput.get().isalpha():  # is seed only letters?
                raise ValueError
            if len(self.seedInput.get()) > 10:
                raise Exception
        except ValueError:
            self.showSeedAlphaErrorMessage()
        except Exception:
            self.showSeedLenErrorMessage()
        else:
            self.mediator.startRandomizer(isoPath, self.startingDeckChecked.get(), self.chestCardsChecked.get(), self.hiddenCardsChecked.get(), self.levelBonusCardsChecked.get(), self.enemyAttributesChecked.get(), self.deckPointChecked.get(), self.writeOptionSelected.get(), self.seedInput.get())

    def showSeedAlphaErrorMessage(self):
        messagebox.showerror('Bad Seed', 'The seed must be alphabetic. No numbers, punctuation, or symbols.')

    def showSeedLenErrorMessage(self):
        messagebox.showerror('Bad Seed', 'The seed must be 10 characters in length or less.')

    def showISOErrorMessage(self):
        messagebox.showerror('File Error', 'Please choose a clean Lost Kingdoms .iso')

    def showDoneMessage(self):
        doneMessage = 'The randomized .iso + log is ready'
        if self.writeOptionSelected.get() == 2:
            doneMessage = 'The randomized .iso is ready'
        if self.writeOptionSelected.get() == 3:
            doneMessage = 'The log is ready'
        messagebox.showinfo('Done', doneMessage)

    def setSeedInputRandom(self):  # todo move to main?
        newSeed = self.seedGenInstance.getSeed()
        self.seedInput.set(newSeed)
