import mmh3
import array
import numpy as np


class ThreeDBF:
    def __init__(self, X, Y, Z, faultTolerance, print_info=True):
        """
        Create a 3D Bloom Filter of size X * Y * Z.
        The faultTolerance must be between 1 and 64, which is the number of bits in the bit array.
        """
        self.createBloomFilter(X, Y, Z)
        self.X = X
        self.Y = Y
        self.Z = Z
        self.inputCount = 0
        self.tau = (64//faultTolerance) * X * Y * Z # C = sigma / alpha, tau = C X  multiplication of dimension
        self.print_info = print_info

    def createBloomFilter(self, X, Y, Z):
        """
        Create the array of size X * Y * Z.
        """
        self.bf = ThreeArray(X, Y, Z)  # create a R-array composed of 0

    def set(self, i, j, k, pos):
        """
        Set the bit of position pos in the bit array to 1, at the indices i, j, k of the filter.
        """
        d = self.bf.get(i, j, k)
        p = 1 << pos
        self.bf.set(i, j, k, d | p)

    def test(self, i, j, k, pos):
        """
        Test the bit of position pos int the bit array, at the indices i, j, k of the filter (if set to 1).
        """
        d = self.bf.get(i, j, k)
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
        pos = h % 63    # Mod 63 (bits), use odd number of bits decrease collision
        if not self.isFull() and not self.testMember(word):
            self.setCount()
            self.set(i, j, k, pos)
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
        pos = h % 63    # Mod 63 (bits), use odd number of bits decrease collision
        return self.test(i, j, k, pos)

    def delete(self, i, j, k, pos):
        """
        Set the bit of position pos in the bit array to 0, at the indices i, j, k of the filter.
        """
        d = self.bf.get(i, j, k)
        p = 1 << pos
        r = d ^ p
        if (p | d) == d:
            self.bf.set(i, j, k, r)

    def deleteMember(self, word):
        """
        Delete a word in the bloom filter. (bit set to 0)
        """
        h = mmh3.hash64(word, seed=42, signed=False)[0]
        i = h % self.X
        j = h % self.Y
        k = h % self.Z
        pos = h % 63
        if self.testMember(word):
            self.delete(i, j, k, pos)
        else:
            if self.print_info:
                print(f"The word : \"{word}\" does not exist")
    
    def __repr__(self):
        """
        Return a representation of the bloom filter.
        """
        return self.bf.__repr__()

class ThreeArray:
    def __init__(self, X, Y, Z):
        """
        Create a matrix of size X * Y * Z, where each value is a bit array of size 64 bits.
        We can get and set each value by giving correct coordinates.
        """
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
        """
        Return a representation of the bloom filter.
        """
        repr = ""
        for i in range(len(self.bf)):
            for j in range(len(self.bf[0])):
                for k in range(len(self.bf[0][0])):
                    repr += str(bin(self.bf[i][j][k])[2:]) + "; "
                repr += "\n"
            repr += "\n"
        return repr
        

if __name__ == "__main__":
    bf = ThreeDBF(31, 37, 41, 4)

    fileName = "DataCleaned.txt"
    with open(fileName, mode="r") as book:
        for word in book.readlines():
            bf.setMember(word[:-1])
