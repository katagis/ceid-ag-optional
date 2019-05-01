import sys
import glob
import re
import math
import timeit
import os
# use Collections Counter. Its the most optimized data structure for what we want to do.
from collections import Counter

# Get a file list from somewhere, you can change this here
def GetFileList(): 
    return glob.glob("./documents/*.txt")

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
        # Use a regex to filter out symbols
        self.wordfreq = MakeDictFromList(re.findall(r"([a-zA-Z0-9\-]+)", file.read()))
        return True

    def GetReadableName(self):
        return os.path.basename(self.filename)[:-4]

    def __repr__(self):
        return self.GetReadableName() + ": " + str(self.wordfreq)

    @staticmethod
    def GetSimilarityBetween(first, second):
        return Dot(first.wordfreq, second.wordfreq) / (Len(first.wordfreq) * Len(second.wordfreq))

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
    print(array)
    size = len(array)
    for i in range(size):
        for j in range(size):
            if i > j:
                val = array[i][j]
            elif i < j:
                val = array[i][j]
            else:
                val = 1.0;
            
            if abs(val - 1) < 0.0001:
                print(("   1    "), end='')
            elif abs(val - 1) > 0.9999:
                print(("   0    "), end='')
            else:
                print(("%f " % val)[1:], end='')
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

if __name__ == "__main__":
    #timeit.timeit("main()")
    main()
    