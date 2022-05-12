import mmh3
import array
import numpy as np


class ThreeDBF:
    def __init__(self, X, Y, Z, faultTolerance):
         # faultTolerance between 1 and 64(numbers of bites)
        self.createBloomFilter(X, Y, Z)
        self.X = X
        self.Y = Y
        self.Z = Z
        self.inputCount = 0
        self.tau = (64//faultTolerance) * X * Y * Z # C = sigma / alpha, tau = C X  multiplication of dimension
        self.alreadyMemberCount = 0

    def createBloomFilter(self, X, Y, Z):
        self.bf = ThreeArray(X, Y, Z)  # create a R-array composed of 0

    def set(self, i, j, k, pos):
        d = self.bf.get(i, j, k)
        p = 1 << pos
        self.bf.set(i, j, k, d | p)

    def test(self, i, j, k, pos):
        d = self.bf.get(i, j, k)
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
        k = h % self.Z
        pos = h % 63    # Mod 63 (bits), use odd number of bits decrease collision
        if not self.isFull() and not self.testMember(word):
            self.setCount()
            self.set(i, j, k, pos)
        else:
            if self.isFull():
                print("Filter is full")
            else:
                print(f"The word : \"{word}\" is already a member of BF")
                self.alreadyMemberCount += 1

    def testMember(self, word):
        flag = True
        h = mmh3.hash64(word, seed=42, signed=False)[0]
        i = h % self.X
        j = h % self.Y
        k = h % self.Z
        pos = h % 63    # Mod 63 (bits), use odd number of bits decrease collision
        flag = self.test(i, j, k, pos)
        return flag

    def delete(self, i, j, k, pos):
        d = self.bf.get(i, j, k)
        p = 1 << pos
        r = d ^ p
        if (p | d) == d:
            self.bf.set(i, j, k, r)

    def deleteMember(self, word):
        h = mmh3.hash64(word, seed=42, signed=False)[0]
        i = h % self.X
        j = h % self.Y
        k = h % self.Z
        pos = h % 63
        if self.testMember(word):
            self.delete(i, j, k, pos)
        else:
            print(f"The word : \"{word}\" does not exist")
    
    def __repr__(self):
        return self.bf.__repr__()

    def getAlreadyMemberCount(self):
        return self.alreadyMemberCount

class ThreeArray:
    def __init__(self, X, Y, Z):
        self.bf = np.array([[0 for _ in range(Y)] for _ in range(X)], dtype=array.array)
        for i in range(X):
            for j in range(Y):
                arr = array.array("Q", (0 for _ in range(Z)))   # Q = Unsigned long long; L = Unsigned long
                self.bf[i][j] = arr     
    
    def get(self, X, Y, Z):
        return self.bf[X][Y][Z]
    
    def set(self, X, Y, Z, value):
        self.bf[X][Y][Z] = value
    
    def __repr__(self):
        repr = ""
        for i in range(len(self.bf)):
            for j in range(len(self.bf[0])):
                for k in range(len(self.bf[0][0])):
                    repr += str(bin(self.bf[i][j][k])[2:]) + "; "
                repr += "\n"
            repr += "\n"
        return repr
        

if __name__ == "__main__":
    bf = ThreeDBF(31, 37, 41, 55)

    fileName = "DataCleaned.txt"
    with open(fileName, mode="r") as book:
        for word in book.readlines():
            bf.setMember(word[:-1])

    print("Already member count : ", bf.getAlreadyMemberCount())