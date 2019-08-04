import random


class SeedGenerator:
    seedCharsFile = 'data/seedChars.txt'

    def __init__(self):
        self.seedChars = []
        with open(self.seedCharsFile, 'r') as file:
            lines = file.readlines()
            for line in lines:
                line = line.rstrip('\r\n')
                self.seedChars.append(line)

    def getSeed(self):
        seed = str()
        for x in range(8):
            randNum = random.randint(0, len(self.seedChars) - 1)
            seed += self.seedChars[randNum]
        return seed
