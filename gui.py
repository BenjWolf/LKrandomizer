import seedGen
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
        self.widgetVars = {'fileInput': tk.StringVar(), 'startingDeckChecked': tk.BooleanVar(), 'chestCardsChecked': tk.BooleanVar(), 'hiddenCardsChecked': tk.BooleanVar(), 'levelBonusCardsChecked': tk.BooleanVar(), 'shopCardsChecked': tk.BooleanVar(), 'fairyCardsChecked': tk.BooleanVar(), 'keyItemsChecked': tk.BooleanVar(), 'enemyAttributesChecked': tk.BooleanVar(), 'escapeBattleChecked': tk.BooleanVar(), 'deckPointChecked': tk.BooleanVar(), 'summonCardChecked': tk.BooleanVar(), 'genIsoSelected': tk.BooleanVar(), 'includeSpoilersSelected': tk.BooleanVar(), 'seedInput': tk.StringVar()}
        self.keyItemsButton = tk.Checkbutton()
        self.makeFileFrame()
        self.makeStartButton()
        self.makeRandomFrame()
        self.makeMiddleFrame()
        self.makeGenerationFrame()

    def makeFileFrame(self):
        # top frame
        topFrame = tk.Frame(self.masterWindow, bd=10)
        topFrame.pack()

        # File selection
        self.widgetVars['fileInput'].set(self.filePath)
        fileEntry = tk.Entry(topFrame, textvariable=self.widgetVars['fileInput'], width=48)
        fileEntry.pack(side='left')

        fileButton = tk.Button(topFrame, text='Select .iso', command=lambda: self.selectISO(fileEntry))
        fileButton.pack(side='left')

    def makeRandomFrame(self):
        # leftmost frame
        randomOptionsFrame = tk.Frame(self.masterWindow, bd=14)
        randomOptionsFrame.pack(side='left', anchor='n')

        optionsLabel = tk.Label(randomOptionsFrame, text='Include random:')
        optionsLabel.pack(anchor='w')

        # Check buttons
        startingDeckButton = tk.Checkbutton(randomOptionsFrame, text='Starting deck', variable=self.widgetVars['startingDeckChecked'])
        startingDeckButton.select()
        startingDeckButton.pack(anchor='w')

        chestButton = tk.Checkbutton(randomOptionsFrame, text='Chest cards', variable=self.widgetVars['chestCardsChecked'], command=lambda: self.chestHiddenItemButtonPressed())
        chestButton.select()
        chestButton.pack(anchor='w')

        hiddenCardsButton = tk.Checkbutton(randomOptionsFrame, text='Hidden cards', variable=self.widgetVars['hiddenCardsChecked'], command=lambda: self.chestHiddenItemButtonPressed())
        hiddenCardsButton.select()
        hiddenCardsButton.pack(anchor='w')

        levelBonusCardsButton = tk.Checkbutton(randomOptionsFrame, text='\'Level Bonus\' cards', variable=self.widgetVars['levelBonusCardsChecked'])
        levelBonusCardsButton.select()
        levelBonusCardsButton.pack(anchor='w')

        shopCardsButton = tk.Checkbutton(randomOptionsFrame, text='Shop cards', variable=self.widgetVars['shopCardsChecked'])
        shopCardsButton.select()
        shopCardsButton.pack(anchor='w')

        fairyCardsButton = tk.Checkbutton(randomOptionsFrame, text='Red fairy rewards', variable=self.widgetVars['fairyCardsChecked'])
        fairyCardsButton.select()
        fairyCardsButton.pack(anchor='w')

        self.keyItemsButton = tk.Checkbutton(randomOptionsFrame, text='Key items', variable=self.widgetVars['keyItemsChecked'])
        self.keyItemsButton.pack(anchor='w')

        enemyAttributeButton = tk.Checkbutton(randomOptionsFrame, text='Enemy attributes', variable=self.widgetVars['enemyAttributesChecked'])
        enemyAttributeButton.pack(anchor='w')

    def makeMiddleFrame(self):
        # Difficulty options
        difficultyFrame = tk.Frame(self.masterWindow, bd=14)
        difficultyFrame.pack(side='left', anchor='n')

        difficultyLabel = tk.Label(difficultyFrame, text='Difficulty:')
        difficultyLabel.pack(anchor='w')

        # Check buttons
        escapeBattleButton = tk.Checkbutton(difficultyFrame, text='Can\'t escape battles', variable=self.widgetVars['escapeBattleChecked'])
        escapeBattleButton.pack(anchor='w')

        deckPointButton = tk.Checkbutton(difficultyFrame, text='Deactivate deck points', variable=self.widgetVars['deckPointChecked'])
        deckPointButton.pack(anchor='w')

        # Other options
        otherLabel = tk.Label(difficultyFrame, text='Other:')
        otherLabel.pack(anchor='w')

        # Check buttons
        summonCardButton = tk.Checkbutton(difficultyFrame, text='Remove summon animations', variable=self.widgetVars['summonCardChecked'])
        summonCardButton.pack(anchor='w')

    def makeGenerationFrame(self):
        # rightmost frame
        rightmostFrame = tk.Frame(self.masterWindow, bd=14)
        rightmostFrame.pack(side='left')

        # seed frame
        seedFrame = tk.Frame(rightmostFrame)
        seedFrame.pack()

        # seed
        seedLabel = tk.Label(seedFrame, text='Seed: ')
        seedLabel.pack(side='left')

        self.setSeedInputRandom()
        seedEntry = tk.Entry(seedFrame, textvariable=self.widgetVars['seedInput'], width=16)
        seedEntry.pack(side='left')

        newSeedButton = tk.Button(rightmostFrame, text='New Seed', command=lambda: self.setSeedInputRandom())
        newSeedButton.pack()

        # output options
        spacerLabel = tk.Label(rightmostFrame, text='')
        spacerLabel.pack(pady=10)

        generationLabel = tk.Label(rightmostFrame, text='Output: ')
        generationLabel.pack(anchor='w')

        # Check buttons
        generateIsoButton = tk.Checkbutton(rightmostFrame, text='Generate .iso', variable=self.widgetVars['genIsoSelected'])
        generateIsoButton.select()
        generateIsoButton.pack(anchor='w')

        includeSpoilersButton = tk.Checkbutton(rightmostFrame, text='Include spoilers in log', variable=self.widgetVars['includeSpoilersSelected'])
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

    def chestHiddenItemButtonPressed(self):
        # if both chest cards and hidden cards unchecked
        if not (self.widgetVars['chestCardsChecked'].get() or self.widgetVars['hiddenCardsChecked'].get()):
            # uncheck key items button and deactivate
            self.keyItemsButton.deselect()
            self.keyItemsButton['state'] = 'disabled'
        else:
            self.keyItemsButton['state'] = 'normal'

    def randomizeButtonPressed(self):
        seed = self.widgetVars['seedInput'].get()
        try:
            if not seed.isalnum():
                raise ValueError
            if len(seed) > 8:
                raise Exception
        except ValueError:
            self.showSeedAlphaErrorMessage()
        except Exception:
            self.showSeedLenErrorMessage()
        else:
            self.mediator.startRandomizer(self.convertWidgetVarsToVals())

    def convertWidgetVarsToVals(self):
        widgetVals = dict()
        for k, v in self.widgetVars.items():
            widgetVals[k] = v.get()
        return widgetVals

    def showSeedAlphaErrorMessage(self):
        messagebox.showerror('Bad Seed', 'The seed must be alphanumeric. No punctuation or symbols.')

    def showSeedLenErrorMessage(self):
        messagebox.showerror('Bad Seed', 'The seed must be 8 characters in length or less.')

    def showISOErrorMessage(self):
        messagebox.showerror('File Error', 'Please choose a clean Lost Kingdoms .iso')

    def showDoneMessage(self):
        doneMessage = 'The patched .iso + log is ready'
        if not self.widgetVars['genIsoSelected'].get():
            doneMessage = 'The log is ready'
        messagebox.showinfo('Done', doneMessage)

    def setSeedInputRandom(self):  # todo move to main?
        newSeed = self.seedGenInstance.getSeed()
        self.widgetVars['seedInput'].set(newSeed)
