import time
import shutil


class FileOutput:
    # filename
    savedPathFile = 'data/savedPath.txt'
    # constants
    gameTitleAppend = {int(b'2d', 16): bytes(b' - RANDOMIZED'), int(b'246C464D', 16): bytes(b' - RANDOMIZED')}
    playerNameAddress = int(b'152838', 16)

    def __init__(self):
        self.newISO = str()
        self.writeAddresses = dict()
        self.writeAddresses.update(self.gameTitleAppend)
        self.logString = str()

    def copyISO(self, isoPath, seed):
        # make copy of .iso with filename @newISO
        self.newISO = 'Lost Kingdoms Randomized ' + seed + '.iso'
        shutil.copy(isoPath, self.newISO)

    def changePlayerNameToSeed(self, seed):
        self.writeAddresses[self.playerNameAddress] = seed.encode('utf-8')  # encode seed to binary

    def writeToISO(self, randomizedDict):
        self.writeAddresses.update(randomizedDict)
        with open(self.newISO, 'r+b') as iso_file:
            for address, value in self.writeAddresses.items():
                iso_file.seek(address)
                iso_file.write(value)

    def writeToLog(self, versionName, seed, optionLog, randLog):
        localTime = time.asctime(time.localtime(time.time()))
        self.logString += versionName + '\n'
        self.logString += 'Randomized on: ' + localTime + '\n'
        self.logString += 'Seed: ' + seed + '\n\n'
        self.logString += optionLog + '\n'
        self.logString += randLog
        logFile = 'log ' + seed + '.txt'
        with open(logFile, 'w') as log:
            log.write(self.logString)

    def saveFilePath(self, isoPath):
        with open(self.savedPathFile, 'w') as file:
            file.write(isoPath)
