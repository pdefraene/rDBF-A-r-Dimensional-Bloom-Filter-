import mmh3
import array
import numpy as np


class FourDBF:
    def __init__(self, X, Y, Z, W, faultTolerance, print_info=True):
        """
        Create a 4D Bloom Filter of size X * Y * Z * W.
        The faultTolerance must be between 1 and 64, which is the number of bits in the bit array.
        """
        self.createBloomFilter(X, Y, Z, W)
        self.X = X
        self.Y = Y
        self.Z = Z
        self.W = W
        self.inputCount = 0
        self.tau = (64//faultTolerance) * X * Y * Z * W # C = sigma / alpha, tau = C X multiplication of dimension
        self.print_info = print_info

    def createBloomFilter(self, X, Y, Z, W):
        """
        Create the array of size X * Y * Z * W
        """
        self.bf = FourArray(X, Y, Z, W)  # create a R-array composed of 0

    def set(self, i, j, k, l, pos):
        """
        Set the bit of position pos in the bit array to 1, at the indices i, j, k, l of the filter.
        """
        d = self.bf.get(i, j, k, l)
        p = 1 << pos
        self.bf.set(i, j, k, l, d | p)

    def test(self, i, j, k, l, pos):
        """
        Test the bit of position pos int the bit array, at the indices i, j, k, l of the filter (if set to 1).
        """
        d = self.bf.get(i, j, k, l)
        p = 1 << pos
        r = d ^ p   # XOR
        t = r & p
        return (t == 0 and d != 0) # Look if the bit is set to one

    def setCount(self):
        """
        Increment the counter of entries and return it
        """
        self.inputCount += 1
        return self.inputCount

    def isFull(self):
        """
        Return true if the bloom filter is full, false otherwise.
        """
        return self.inputCount == self.tau

    def setMember(self, word):
        """
        Add a word in the bloom filter, meaning set the corresponding bit to 1.
        This is done in non-blind insertion, which means we look if the word is already in the bloom filter before inserting.
        """
        h = mmh3.hash64(word, seed=42, signed=False)[0]
        i = h % self.X
        j = h % self.Y
        k = h % self.Z
        l = h % self.W
        pos = h % 63    # Mod 63 (bits), use odd number of bits decrease collision
        if not self.isFull() and not self.testMember(word):
            self.setCount()
            self.set(i, j, k, l, pos)
        else:
            if self.isFull():
                if self.print_info:
                    print("Filter is full")
            else:
                if self.print_info:
                    print(f"The word : \"{word}\" is already a member of BF")

    def testMember(self, word):
        """
        Test if a word is in the bloom filter. (bit set to 1)
        """
        h = mmh3.hash64(word, seed=42, signed=False)[0]
        i = h % self.X
        j = h % self.Y        
        k = h % self.Z
        l = h % self.W
        pos = h % 63    # Mod 63 (bits), use odd number of bits decrease collision
        return self.test(i, j, k, l, pos)

    def delete(self, i, j, k, l, pos):
        """
        Set the bit of position pos in the bit array to 0, at the indices i, j, k, l of the filter.
        """
        d = self.bf.get(i, j, k, l)
        p = 1 << pos
        r = d ^ p
        if (p | d) == d:
            self.bf.set(i, j, k, l, r)

    def deleteMember(self, word):
        """
        Delete a word in the bloom filter. (bit set to 0)
        """
        h = mmh3.hash64(word, seed=42, signed=False)[0]
        i = h % self.X
        j = h % self.Y
        k = h % self.Z
        l = h % self.W
        pos = h % 63
        if self.testMember(word):
            self.delete(i, j, k, l, pos)
        else:
            if self.print_info:
                print(f"The word : \"{word}\" does not exist")
    
    def __repr__(self):
        """
        Return a representation of the bloom filter.
        """
        return self.bf.__repr__()

class FourArray:
    def __init__(self, X, Y, Z, W):
        """
        Create a matrix of size X * Y * Z * W, where each value is a bit array of size 64 bits.
        We can get and set each value by giving correct coordinates.
        """
        self.bf = np.array([[[0 for _ in range(Z)] for _ in range(Y)] for _ in range(X)], dtype=array.array)
        for i in range(X):
            for j in range(Y):
                for k in range(Z):
                    arr = array.array("Q", (0 for _ in range(W)))   # Q = Unsigned long long; L = Unsigned long
                    self.bf[i][j][k] = arr     
    
    def get(self, X, Y, Z, W):
        return self.bf[X][Y][Z][W]
    
    def set(self, X, Y, Z, W, value):
        self.bf[X][Y][Z][W] = value
    
    def __repr__(self):
        """
        Return a representation of the bloom filter.
        """
        repr = ""
        for i in range(len(self.bf)):
            for j in range(len(self.bf[0])):
                for k in range(len(self.bf[0][0])):
                    for l in range(len(self.bf[0][0][0])):
                        repr += str(bin(self.bf[i][j][k][l])[2:]) + "; "
                    repr += "\n"
                repr += "\n"
            repr += "\n"
        return repr
        

if __name__ == "__main__":
    bf = FourDBF(31, 37, 41, 43, 4)

    fileName = "DataCleaned.txt"
    with open(fileName, mode="r") as book:
        for word in book.readlines():
            bf.setMember(word[:-1])
