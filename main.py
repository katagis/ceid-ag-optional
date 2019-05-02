import sys
import glob
import re
import math
import timeit
import os


# Get a file list from somewhere, you can change this here
def GetFileList(): 
    return glob.glob("./documents/*.txt")

# matching regex
def GetRegex():
    #return r"([a-zA-Z0-9\-]+)"
    return r"(\w+)"

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
        c2val = c2.get(key, None)
        # if key exists in both (word found in both texts)
        if c2val:
            # increase sum
            total += val * c2val
    # all keys not included in one of c1 or c2 do not affect the total sum (freq * 0 == 0)
    return total

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

    def __repr__(self):
        return self.GetReadableName() + ": " + str(self.wordfreq)

    @staticmethod
    def GetSimilarityBetween(first, second):
        return Dot(first.wordfreq, second.wordfreq) / (Len(first.wordfreq) * Len(second.wordfreq))

class Similarity:
    def __init__(self, entry1, entry2):
        self.entry1 = entry1
        self.entry2 = entry2
        self.similar = TextEntry.GetSimilarityBetween(entry1, entry2)

    def __repr__(self):
        return str(self) + "\n"

    def __str__(self):
        return self.entry1.GetReadableName().ljust(24) + " | " + self.entry2.GetReadableName().ljust(24) + " : " + str(self.similar)
    

def DescSimilarity(a, b):
    return 1 if a.similar > b.similar else -1

# tirnangular array containing all similarities
def Make2DArray(entries):
    size = len(entries)
    array = []
    for i in range(size):
        array.append([0] * size)
        for j in range(i + 1, size):
            array[i][j] = TextEntry.GetSimilarityBetween(entries[i], entries[j])
    return array

def UtilPrintTriangle(array):
    size = len(array)
    for i in range(size):
        for j in range(size):
            if i > j:
                val = array[j][i]
            elif i < j:
                val = array[i][j]
            else:
                val = 1.0
            
            if abs(val - 1) < 0.0001:
                print(("   1    "), end='')
            elif abs(val - 1) > 0.9999:
                print(("   0    "), end='')
            else:
                print(("%f " % val)[1:], end='')
        print()


def MakeArray2(entries):
    return [[Similarity(entries[i], entries[j]) for j in range(i + 1, len(entries))] for i in range(len(entries))]
    
def PrintTriangle2(array):
    for subarray in array:
        for val in subarray:
            print(("%f " % val.similar)[1:], end='')
        print()


# Get a list of filepaths and read them as our data.
def ReadFiles(filenames):
    entries = []
    for filename in filenames:
        entry = TextEntry(filename)
        if entry.ReadData():
            entries.append(entry)
    return entries

def main():
    filenames = GetFileList()
    if (len(filenames) == 0):
        print("No files found. Exiting...")
        exit
    
    entries = ReadFiles(filenames)
    UtilPrintTriangle(Make2DArray(entries))
    print()
    similar = MakeArray2(entries)

    similarlinear = [item for items in similar for item in items]
    print(similarlinear)


if __name__ == "__main__":
    #timeit.timeit("main()")
    main()
    