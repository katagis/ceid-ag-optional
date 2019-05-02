import sys
import glob
import re
import math
import os

# Get a file list from somewhere, use argv[1] if exists.
def GetFileList():
    try:
        globfilter = sys.argv[1]
    except:
        globfilter = "./documents/*.txt"
    return glob.glob(globfilter)

# matching regex, can be u
def GetRegex():
    #return r"([a-zA-Z0-9\-]+)"
    return r"(\w+)"

# Return "|| d ||" length
def Len(d):
    x = 0
    for elem in d.values():
        x += elem**2
    return math.sqrt(x)

# Expects 2 Dicts, produces d1 * d2 as defined in assignment
# dict is of type {"word": TimesFound}
def Dot(c1, c2):
    total = 0
    for key, val in c1.items():
        c2val = c2.get(key, 0) # get 0 if not exists
        total += val * c2val
    return total

# Read a list of words and convert them to a frequency dictionary
def MakeDictFromList(wordlist):
    vec = {}
    for word in wordlist:
        wlow = word.lower()
        if wlow not in vec:
            vec[wlow] = 1
        else:
            vec[wlow] += 1
    return vec

class TextEntry:
    def __init__(self, filename):
        self.filename = filename

    def ReadData(self):
        try:
            file = open(self.filename, "r")
        except:
            print("Failed to open file: " + self.filename + " (skipping)")
            return False
        # Use a regex to filter out symbols, save to a word freq dictionary.
        self.wordfreq = MakeDictFromList(re.findall(GetRegex(), file.read()))
        return True

    def GetReadableName(self):
        return os.path.basename(self.filename)[:-4]

    @staticmethod
    def GetSimilarityBetween(first, second):
        return Dot(first.wordfreq, second.wordfreq) / (Len(first.wordfreq) * Len(second.wordfreq))

# Get a list of filepaths and read them as our data.
def ReadFiles(filenames):
    entries = []
    for filename in filenames:
        entry = TextEntry(filename)
        # skip an entry if we could not read the file
        if entry.ReadData():
            entries.append(entry)
    return entries

class Similarity:
    def __init__(self, entry1, entry2):
        self.entry1 = entry1
        self.entry2 = entry2
        self.similar = TextEntry.GetSimilarityBetween(entry1, entry2)

    def GetReadable(self, padding=24):
        return self.entry1.GetReadableName().ljust(padding) + " - " + self.entry2.GetReadableName().ljust(padding) + " : %1.4f" % self.similar

    # printing utility
    def MaxEntrySize(self):
        return max(len(self.entry1.GetReadableName()), len(self.entry2.GetReadableName()))

    @staticmethod
    def PrintList(similarities, stopOnZero=False):
        # find max size of filename, use it as padding when printing to get a nice output result
        padding = max(similarities, key=lambda sim: sim.MaxEntrySize()).MaxEntrySize()
        for item in similarities:
            if stopOnZero and item.similar == 0:
                return
            print(item.GetReadable(padding))

# Create similiarity objects and and sort them by similarity in a 1d array
def MakeSimilarities(entries):
    similarities = [Similarity(entries[i], entries[j])
        # iterate all: 0 < i < size, i < j < size (triangular array)
        for i in range(len(entries)) 
        for j in range(i + 1, len(entries))
    ]
    return sorted(similarities, key=lambda sim: sim.similar, reverse=True)

def main():
    filenames = GetFileList()

    try: 
        k = int(sys.argv[2])
    except:
        k = 0

    if (len(filenames) == 0):
        print("No files found. Exiting...")
        exit(-1)

    print("Including " + str(len(filenames)) + " files:")
    for filename in filenames:
        print(filename)
    print()

    entries = ReadFiles(filenames)
    similarities = MakeSimilarities(entries)

    if k <= 0:
        Similarity.PrintList(similarities, stopOnZero = True)
    else:
        Similarity.PrintList(similarities[:k])

if __name__ == "__main__":
    main()
    