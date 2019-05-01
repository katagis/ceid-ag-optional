import sys
import glob
import re
import math
# use Collections Counter. Its the most optimized data structure for what we want to do.
from collections import Counter

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


def ReadFiles(filenames):
    data = {}
    for filename in filenames:
        try:
            file = open(filename, "r")
        except:
            print("Failed to open file: " + filename + " (skipping)")
            continue
        # Use a regex to filter out symbols
        data[filename] = MakeDictFromList(re.findall(r"([a-zA-Z0-9\-]+)", file.read()))
    return data

# Return "|| d ||" length
def VecLen(vec):
    x = 0
    for elem in vec.values():
        x += elem**2
    return math.sqrt(x)

# Expects 2 Dicts
def Dot(c1, c2):
    total = 0
    for key in c1:
        c2val = c2.get(key, None)
        if c2val:
            total += c1[key] * c2val
    return total;


# Get cos(d1, d2) similarity, expects Dictionary objects.
def GetSimilarity(d1, d2):
    return Dot(d1, d2) / (VecLen(d1) * VecLen(d2))


def main():
    filenames = GetFileList()
    if (len(filenames) == 0):
        print("No files found. Exiting...")
        exit
    
    data = ReadFiles(filenames)
    c1 = data[filenames[0]]
    c2 = data[filenames[1]]
    
    z = GetSimilarity(c1, c2)
    print(z)





if __name__ == "__main__":
    main()