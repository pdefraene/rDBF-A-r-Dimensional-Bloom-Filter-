import mmh3
import array
import numpy as np
from cuckoopy import CuckooFilter 
import sys


class TwoDBF:
    def __init__(self, X, Y, faultTolerance, print_info=True):
        # faultTolerance between 1 and 64 (numbers of bits)
        self.createBloomFilter(X, Y)
        self.X = X
        self.Y = Y
        self.inputCount = 0
        self.tau = (64//faultTolerance) * X * Y # C = sigma / alpha, tau = C X multiplication of dimension
        self.alreadyMemberCount = 0
        self.print_info = print_info

    def createBloomFilter(self, X, Y):
        self.bf = TwoArray(X, Y)  # create a R-array composed of 0

    def set(self, i, j, pos):
        d = self.bf.get(i, j)
        p = 1 << pos
        self.bf.set(i, j, d | p)

    def test(self, i, j, pos):
        d = self.bf.get(i, j)
        p = 1 << pos
        r = d ^ p   # XOR
        t = r & p
        if t == 0 and d != 0:   # Bit is set to one
            return True
        return False

    def setCount(self):
        self.inputCount += 1
        return self.inputCount

    def isFull(self):
        if self.inputCount != self.tau:
            return False
        return True

    def setMember(self, word):
        """
        non-blind insertion
        """
        h = mmh3.hash64(word, seed=42, signed=False)[0]
        i = h % self.X
        j = h % self.Y
        pos = h % 63    # Mod 63 (bits), use odd number of bits decrease collision
        if not self.isFull() and not self.testMember(word):
            self.setCount()
            self.set(i, j, pos)
        else:
            if self.isFull():
                if self.print_info:
                    print("Filter is full")
            else:
                if self.print_info:
                    print(f"The word : \"{word}\" is already a member of BF")
                self.alreadyMemberCount += 1

    def testMember(self, word):
        flag = True
        h = mmh3.hash64(word, seed=42, signed=False)[0]
        i = h % self.X
        j = h % self.Y
        pos = h % 63    # Mod 63 (bits), use odd number of bits decrease collision
        flag = self.test(i, j, pos)
        return flag

    def delete(self, i, j, pos):
        d = self.bf.get(i, j)
        p = 1 << pos
        r = d ^ p
        if (p | d) == d:
            self.bf.set(i, j, r)

    def deleteMember(self, word):
        h = mmh3.hash64(word, seed=42, signed=False)[0]
        i = h % self.X
        j = h % self.Y
        pos = h % 63
        if self.testMember(word):
            self.delete(i, j, pos)
        else:
            if self.print_info:
                print(f"The word : \"{word}\" does not exist")
    
    def __repr__(self):
        return self.bf.__repr__()

    def getAlreadyMemberCount(self):
        return self.alreadyMemberCount

class TwoArray:
    def __init__(self, X, Y):
        self.bf = np.array([0 for _ in range(X)], dtype=array.array)
        for i in range(X):
            arr = array.array("Q", (0 for _ in range(Y)))   # Q = Unsigned long long; L = Unsigned long
            self.bf[i] = arr     
    
    def get(self, X, Y):
        return self.bf[X][Y]
    
    def set(self, X, Y, value):
        self.bf[X][Y] = value
    
    def nbBits(self):
        arraySize = sys.getsizeof(self.bf[0])
        itemSize = self.bf.itemsize

        print("arraySize", arraySize)
        print(arraySize*len(self.bf))
        print(itemSize)
        
    def __repr__(self):
        repr = ""
        for i in range(len(self.bf)):
            for j in range(len(self.bf[0])):
                repr += str(bin(self.bf[i][j])[2:]) + "; "
            repr += "\n"
        return repr
        

if __name__ == "__main__":
    bloom = TwoDBF(31, 37, 4)

    for i in range(80):
        bloom.setMember(str(i))

    print(bloom)
    bloom.bf.nbBits()
