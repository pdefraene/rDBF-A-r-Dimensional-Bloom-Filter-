from TwoDBF import TwoDBF
from plot import *


def ProofFalseNegative():
    """
    Show the false negative error
    """
    bloom = TwoDBF(2,3,4,True)
    print("Creating a 2D-Bloom Filter of size : 2*3")
    print("Add 5 in the Bloom Filter")
    bloom.setMember("5")
    print("Add 11 in the Bloom Filter")
    bloom.setMember("11")
    print("Delete 5 in the Bloom Filter")
    bloom.deleteMember("5")
    print("Test if 11 is in the Bloom Filter: " , bloom.testMember("11"))


if __name__ == "__main__":
    ProofFalseNegative()
    