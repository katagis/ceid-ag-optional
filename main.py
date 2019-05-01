import sys
import glob
import re
# use Collections Counter. Its the most optimized data structure for what we want to do.
from collections import Counter

def GetFileList(): 
    return glob.glob("./documents/*.txt")

# Read a list of words and convert them to a frequency dictionary
def MakeCounterFromList(wordlist):
    vec = Counter()
    for word in wordlist:
        vec[word.lower()] += 1
    return vec


def ReadFilesIntoCounters(filenames):
    data = {}
    for filename in filenames:
        try:
            file = open(filename, "r")
        except:
            print("Failed to open file: " + filename + " (skipping)")
            continue
        # Use a regex to filter out symbols
        data[filename] = MakeCounterFromList(re.findall(r"([a-zA-Z0-9\-]+)", file.read()))
    return data

# Return "|| d ||" length
def VecLen(vec):
    x = 0
    for elem in vec:
        x += elem**2
    return sqrt(x)

# Don't forget to intersect the 2 Counters before calling this to align the data.
# intersection can be performed since we only care about elements that exist in both sets
#   (all others are 0*x == 0)
# Expects 2 arrays of the same size
def VecDot(vec1, vec2):
    if len(vec1) != vev2:
        raise "VecDot expects same size vectors."
    return 


# Get cos(d1, d2) similarity, expects Counter objects.
def GetSimilarity(d1, d2):


            

def main():
    filenames = GetFileList()
    if (len(filenames) == 0):
        print("No files found. Exiting...")
        exit
    
    data = ReadFilesIntoCounters(filenames)





if __name__ == "__main__":
    main()