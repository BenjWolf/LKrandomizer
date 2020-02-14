import seedGen
import classes
import tkinter as tk
import tkinter.filedialog as fdialog
import tkinter.messagebox as messagebox


class GUI:

    def __init__(self, mediator, masterWindow, savedFilePath, versionName):
        self.mediator = mediator
        self.masterWindow = masterWindow
        self.masterWindow.title(versionName)
        self.masterWindow.resizable('false', 'false')
        self.seedGenInstance = seedGen.SeedGenerator()
        self.filePath = savedFilePath
        self.widgetVars = classes.WidgetVars()
        self.keyItemsButton = tk.Checkbutton()
        self.itemHintsButton = tk.Checkbutton()
        self.itemHiddenCardButton = tk.Checkbutton()
        self.makeFileFrame()
        self.makeStartButton()
        self.makeLeftFrame()
        self.makeMiddleFrame()
        self.makeRightFrame()

    def makeFileFrame(self):
        # top frame
        topFrame = tk.Frame(self.masterWindow, bd=10)
        topFrame.pack()

        # File selection
        self.widgetVars.fileInput.set(self.filePath)
        fileEntry = tk.Entry(topFrame, textvariable=self.widgetVars.fileInput, width=48)
        fileEntry.pack(side='left')

        fileButton = tk.Button(topFrame, text='Select .iso', command=lambda: self.selectISO(fileEntry))
        fileButton.pack(side='left')

    def makeLeftFrame(self):
        # leftmost frame
        leftFrame = tk.Frame(self.masterWindow, bd=14)
        leftFrame.pack(side='left', anchor='n')

        optionsLabel = tk.Label(leftFrame, text='Include random:')
        optionsLabel.pack(anchor='w')

        # Check buttons
        startingDeckButton = tk.Checkbutton(leftFrame, text='Starting deck', variable=self.widgetVars.startingDeckChecked)
        startingDeckButton.select()
        startingDeckButton.pack(anchor='w')

        chestButton = tk.Checkbutton(leftFrame, text='Chest cards', variable=self.widgetVars.chestCardsChecked, command=lambda: self.updateKeyItemsButton())
        chestButton.select()
        chestButton.pack(anchor='w')

        hiddenCardsButton = tk.Checkbutton(leftFrame, text='Hidden cards', variable=self.widgetVars.hiddenCardsChecked, command=lambda: self.updateKeyItemsButton())
        hiddenCardsButton.select()
        hiddenCardsButton.pack(anchor='w')

        levelBonusCardsButton = tk.Checkbutton(leftFrame, text='\'Level Bonus\' cards', variable=self.widgetVars.levelBonusCardsChecked)
        levelBonusCardsButton.select()
        levelBonusCardsButton.pack(anchor='w')

        shopCardsButton = tk.Checkbutton(leftFrame, text='Shop cards', variable=self.widgetVars.shopCardsChecked)
        shopCardsButton.select()
        shopCardsButton.pack(anchor='w')

        fairyCardsButton = tk.Checkbutton(leftFrame, text='Red fairy rewards', variable=self.widgetVars.fairyCardsChecked)
        fairyCardsButton.select()
        fairyCardsButton.pack(anchor='w')

        enemyAttributeButton = tk.Checkbutton(leftFrame, text='Enemy attributes', variable=self.widgetVars.enemyAttributesChecked)
        enemyAttributeButton.pack(anchor='w')

    def makeMiddleFrame(self):
        middleFrame = tk.Frame(self.masterWindow, bd=14)
        middleFrame.pack(side='left', anchor='n')

        # Key items
        keyItemsLabel = tk.Label(middleFrame, text='Key Items:')
        keyItemsLabel.pack(anchor='w')

        self.keyItemsButton = tk.Checkbutton(middleFrame, text='Random location', variable=self.widgetVars.keyItemsChecked, command=lambda: self.updateItemOptions())
        self.keyItemsButton.pack(anchor='w')

        self.itemHintsButton = tk.Checkbutton(middleFrame, text='NPCs give hints', variable=self.widgetVars.itemHintsChecked, state='disabled')
        self.itemHintsButton.pack(anchor='w')

        ''' Remove option for hidden cards to be items until bug fix regarding active object
        self.itemOption = tk.Checkbutton(middleFrame, text='Allow hidden cards to be items', variable=self.widgetVars.itemHiddenCardChecked, state='disabled')
        self.itemOption.pack(anchor='w')
        '''
        # spacer
        tk.Label(middleFrame, text='').pack()

        # Difficulty options

        difficultyLabel = tk.Label(middleFrame, text='Difficulty:')
        difficultyLabel.pack(anchor='w')

        # Check buttons
        escapeBattleButton = tk.Checkbutton(middleFrame, text='Can\'t escape battles', variable=self.widgetVars.escapeBattleChecked)
        escapeBattleButton.pack(anchor='w')

        deckPointButton = tk.Checkbutton(middleFrame, text='Deactivate deck points', variable=self.widgetVars.deckPointChecked)
        deckPointButton.pack(anchor='w')

        fairPlayButton = tk.Checkbutton(middleFrame, text='Fair Play cards only', variable=self.widgetVars.fairPlay)
        fairPlayButton.pack(anchor='w')

        # spacer
        tk.Label(middleFrame, text='').pack()

        # Other options
        otherLabel = tk.Label(middleFrame, text='Other:')
        otherLabel.pack(anchor='w')

        # Check buttons
        lk2CardButton = tk.Checkbutton(middleFrame, text='LKII card changes', variable=self.widgetVars.lk2CardChecked)
        lk2CardButton.pack(anchor='w')

        lk2EnemyButton = tk.Checkbutton(middleFrame, text='LKII enemy changes', variable=self.widgetVars.lk2EnemyChecked)
        lk2EnemyButton.pack(anchor='w')

    def makeRightFrame(self):
        # rightmost frame
        rightFrame = tk.Frame(self.masterWindow, bd=14)
        rightFrame.pack(side='left')

        # randomization style
        randomizationStyleLabel = tk.Label(rightFrame, text='Randomization style: ')
        randomizationStyleLabel.pack(anchor='w')

        # radio buttons
        fullRandomButton = tk.Radiobutton(rightFrame, text='Full random', variable=self.widgetVars.randomStyle, value = 1)
        fullRandomButton.select()
        fullRandomButton.pack(anchor='w')

        balancedButton = tk.Radiobutton(rightFrame, text='Balanced', variable=self.widgetVars.randomStyle, value = 2)
        balancedButton.pack(anchor='w')

        # spacer
        tk.Label(rightFrame, text='').pack()

        # seed frame
        seedFrame = tk.Frame(rightFrame)
        seedFrame.pack()

        # seed
        seedLabel = tk.Label(seedFrame, text='Seed: ')
        seedLabel.pack(side='left')

        self.setSeedInputRandom()
        seedEntry = tk.Entry(seedFrame, textvariable=self.widgetVars.seedInput, width=16)
        seedEntry.pack(side='left')

        newSeedButton = tk.Button(rightFrame, text='New Seed', command=lambda: self.setSeedInputRandom())
        newSeedButton.pack()

        # spacer
        tk.Label(rightFrame, text='').pack()

        # output options
        generationLabel = tk.Label(rightFrame, text='Output: ')
        generationLabel.pack(anchor='w')

        # Check buttons
        generateIsoButton = tk.Checkbutton(rightFrame, text='Generate .iso', variable=self.widgetVars.genIsoSelected)
        generateIsoButton.select()
        generateIsoButton.pack(anchor='w')

        includeSpoilersButton = tk.Checkbutton(rightFrame, text='Include spoilers in log', variable=self.widgetVars.includeSpoilersSelected)
        includeSpoilersButton.pack(anchor='w')

    def makeStartButton(self):
        # bottom frame
        bottomFrame = tk.Frame(self.masterWindow, bd=12)
        bottomFrame.pack(side='bottom')
        # start button
        randomizeButton = tk.Button(bottomFrame, text='Start Randomization', bg='#65c421', activebackground='yellow', command=lambda: self.randomizeButtonPressed())
        randomizeButton.pack()

    def selectISO(self, fileEntry):
        filename = fdialog.askopenfilename(initialdir='/', title='Select file', filetypes=(('ISO files', '*.iso'), ('all files', '*.*')))
        length = len(fileEntry.get())
        fileEntry.delete(0, length)  # clear text
        fileEntry.insert(0, filename)  # insert text to textbox

    def updateKeyItemsButton(self):
        # if chest cards unchecked
        if not (self.widgetVars.chestCardsChecked.get()):
            # uncheck key items button and deactivate
            self.keyItemsButton.deselect()
            self.keyItemsButton['state'] = 'disabled'
            self.updateItemOptions()
        else:
            self.keyItemsButton['state'] = 'normal'
            self.updateItemOptions()


    def updateItemOptions(self):
        if self.widgetVars.keyItemsChecked.get():
            self.itemHintsButton['state'] = 'normal'
            if self.widgetVars.hiddenCardsChecked.get():
                self.itemHiddenCardButton['state'] = 'normal'
            else:
                self.itemHiddenCardButton.deselect()
                self.itemHiddenCardButton['state'] = 'disabled'
        else:
            self.itemHintsButton.deselect()
            self.itemHintsButton['state'] = 'disabled'
            self.itemHiddenCardButton.deselect()
            self.itemHiddenCardButton['state'] = 'disabled'

    def randomizeButtonPressed(self):
        seed = self.widgetVars.seedInput.get()
        try:
            if not seed.isalnum():  # is seed alpha-numeric?
                raise ValueError
            if len(seed) > 8:  # is seed 8 chars or less?
                raise Exception
        except ValueError:
            self.showSeedAlphaErrorMessage()
        except Exception:
            self.showSeedLenErrorMessage()
        else:
            self.mediator.startRandomizer(self.widgetVars)

    def showSeedAlphaErrorMessage(self):
        messagebox.showerror('Bad Seed', 'The seed must be alphanumeric. No punctuation or symbols.')

    def showSeedLenErrorMessage(self):
        messagebox.showerror('Bad Seed', 'The seed must be 8 characters in length or less.')

    def showISOErrorMessage(self):
        messagebox.showerror('File Error', 'Please choose a clean Lost Kingdoms .iso')

    def showDoneMessage(self):
        doneMessage = 'The patched .iso + log is ready'
        if not self.widgetVars.genIsoSelected.get():
            doneMessage = 'The log is ready'
        messagebox.showinfo('Done', doneMessage)

    def setSeedInputRandom(self):  # todo move to main?
        newSeed = self.seedGenInstance.getSeed()
        self.widgetVars.seedInput.set(newSeed)
