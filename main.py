from cuckoopy import CuckooFilter
import time
import sys

from TwoDBF import TwoDBF
from ThreeDBF import ThreeDBF
from FourDBF import FourDBF


if __name__ == "__main__":

    cuckooFilter = CuckooFilter(capacity=100000, bucket_size=10000, fingerprint_size=1000)
    start_cuckoo = time.time()
    fileName = "DataCleaned3.txt"
    with open(fileName, mode="r") as book:
        for word in book.readlines():
            cuckooFilter.insert(word[:-1])
    end_cuckoo = time.time()

    bloom = TwoDBF(31, 37, 4)
    start_bloom = time.time()
    fileName = "DataCleaned3.txt"
    with open(fileName, mode="r") as book:
        for word in book.readlines():
            bloom.setMember(word[:-1])
    end_bloom = time.time()

    print("Cuckoo time : ", end_cuckoo-start_cuckoo)
    print("Bloom time : ", end_bloom-start_bloom)
    print(sys.getsizeof(cuckooFilter.buckets))
    bloom.bf.nbBits()


    """
    unique_words = {}
    different_words = []
    similar_word = 0
    total = 0
    fileName = "DataCleaned3.txt"
    with open(fileName, mode="r") as book:
        for word in book.readlines():
            # bloom.setMember(word[:-1])
            if word not in different_words:
                unique_words[word] = 1
                different_words.append(word)
            else:
                similar_word += 1
                unique_words[word] += 1
            total += 1

    number_unique_words = 0
    for i in unique_words.keys():
        if unique_words[i] == 1:
            number_unique_words += 1

    print("number unique words : ", number_unique_words)
    print("number different words : ", len(different_words))
    print("number similar words : ", similar_word)
    print("total number words : ", total)
    """

    # DataCleaned1 (one part)
    # Total number of words : 17001
    # Number of unique words : 1271
    # Number of different words : 2570
    # Number of similar words : 14431

    # Two array : 14473
    # Three array : 14431
    # Four array : 14430
    # Five array : 14431
    # ===

    # DataCleaned2 (two parts)
    # Total number of words : 34715
    # Number of unique words : 1764
    # Number of different words : 3894
    # Number of similar words : 30821

    # Two array : 
    # Three array : 
    # Four array : 
    # Five array : 
    # ===

    # DataCleaned3 (all book)
    # Total number of words : 95775
    # Number of unique words : 2890
    # Number of different words : 6978
    # Number of similar words : 88797

    # Two array : 89106
    # Three array : 
    # Four array : 
    # Five array : 