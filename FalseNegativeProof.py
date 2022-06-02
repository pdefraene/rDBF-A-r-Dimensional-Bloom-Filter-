import time
import random
import mmh3

import operator as op
from functools import reduce

from cuckoopy import CuckooFilter
from bloom_filter import BloomFilter

from TwoDBF import TwoDBF
from ThreeDBF import ThreeDBF
from FourDBF import FourDBF
from FiveDBF import FiveDBF
from plot import *

if __name__ == "__main__":
    bloom = TwoDBF(2,3,4,True)
    print("Creating a 2D-Bloom Filter of size : 2*3")
    #bloom.setMember("0")
    #bloom.setMember("1")
    #bloom.setMember("2")
    #bloom.setMember("3")
    #bloom.setMember("4")
    bloom.setMember("5")
    print("Add 5 in the Bloom Filter")
    #bloom.setMember("6")
    #bloom.setMember("7")
    #bloom.setMember("8")
    #bloom.setMember("9")
    #bloom.setMember("10")
    bloom.setMember("11")
    print("Add 11 in the Bloom Filter")
    bloom.deleteMember("5")
    print("delete 5 in the Bloom Filter")
    print("test if 11 is in the Bloom Filter: " , bloom.testMember("11"))