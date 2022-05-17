import time

import operator as op
from functools import reduce


from cuckoopy import CuckooFilter
from bloom_filter import BloomFilter

from TwoDBF import TwoDBF
from ThreeDBF import ThreeDBF
from FourDBF import FourDBF
from FiveDBF import FiveDBF
from plot import *


def count_words():
    unique_words = {}
    different_words = []
    similar_word = 0
    total = 0
    fileName = "DataCleaned3.txt"
    with open(fileName, mode="r") as book:
        for word in book.readlines():
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


"""
Processing time
"""
def check_processing_time_cuckoo(filter, fileName):
    with open(fileName, mode="r") as book:
        start_time = time.time()
        for word in book.readlines():
            filter.insert(word[:-1])
    end_time = time.time()
    return end_time - start_time


def check_processing_time_bloom_simple(filter, fileName):
    with open(fileName, mode="r") as book:
        start_time = time.time()
        for word in book.readlines():
            filter.add(word[:-1])
    end_time = time.time()
    return end_time - start_time


def check_processing_time_bloom(filter, fileName):
    with open(fileName, mode="r") as book:
        start_time = time.time()
        for word in book.readlines():
            filter.setMember(word[:-1])
    end_time = time.time()
    return end_time - start_time


def compare_processing_times():
    """
    Compare the total processing time taken by all filters on a given dataset.
    """
    bloom_2 = TwoDBF(31, 37, 4, print_info=False)
    bloom_3 = ThreeDBF(31, 37, 41, 4, print_info=False)
    bloom_4 = FourDBF(31, 37, 41, 43, 4, print_info=False)
    bloom_5 = FiveDBF(31, 37, 41, 43, 47, 4, print_info=False)
    bloom_simple = BloomFilter(max_elements=100000, error_rate=0.001)
    cuckoo_filter = CuckooFilter(capacity=100000, bucket_size=10000, fingerprint_size=1000)
    fileName = "DataCleaned3.txt"

    processing_times = []
    processing_times.append(check_processing_time_bloom(bloom_2, fileName))
    processing_times.append(check_processing_time_bloom(bloom_3, fileName))
    processing_times.append(check_processing_time_bloom(bloom_4, fileName))
    processing_times.append(check_processing_time_bloom(bloom_5, fileName))    
    processing_times.append(check_processing_time_bloom_simple(bloom_simple, fileName))
    processing_times.append(check_processing_time_cuckoo(cuckoo_filter, fileName))
    names = ["2DBF", "3DBF", "4DBF", "5DBF", "Simple Bloom", "Cuckoo"]

    plot_processing_times(processing_times, names)


"""
Insertion time
"""
def check_insertion_time_cuckoo(filter, fileName):
    all_insertion_times = []
    with open(fileName, mode="r") as book:
        for word in book.readlines():
            start_time = time.time()
            filter.insert(word[:-1])
            end_time = time.time()
            all_insertion_times.append(end_time - start_time)
    insertion_time = sum(all_insertion_times)/len(all_insertion_times)
    return insertion_time


def check_insertion_time_bloom_simple(filter, fileName):
    all_insertion_times = []
    with open(fileName, mode="r") as book:
        for word in book.readlines():
            start_time = time.time()
            filter.add(word[:-1])
            end_time = time.time()
            all_insertion_times.append(end_time - start_time)
    insertion_time = sum(all_insertion_times)/len(all_insertion_times)
    return insertion_time


def check_insertion_time_bloom(filter, fileName):
    all_insertion_times = []
    with open(fileName, mode="r") as book:
        for word in book.readlines():
            start_time = time.time()
            filter.setMember(word[:-1])
            end_time = time.time()
            all_insertion_times.append(end_time - start_time)
    insertion_time = sum(all_insertion_times)/len(all_insertion_times)
    return insertion_time


def compare_insertion_time():
    """
    Compare how much time every insertion takes for every filter on a given dataset.
    """
    bloom_2 = TwoDBF(31, 37, 4, print_info=False)
    bloom_3 = ThreeDBF(31, 37, 41, 4, print_info=False)
    bloom_4 = FourDBF(31, 37, 41, 43, 4, print_info=False)
    bloom_5 = FiveDBF(31, 37, 41, 43, 47, 4, print_info=False)
    bloom_simple = BloomFilter(max_elements=100000, error_rate=0.001)
    cuckoo_filter = CuckooFilter(capacity=100000, bucket_size=10000, fingerprint_size=1000)
    fileName = "DataCleaned3.txt"

    insertion_times = []
    insertion_times.append(check_insertion_time_bloom(bloom_2, fileName))
    insertion_times.append(check_insertion_time_bloom(bloom_3, fileName))
    insertion_times.append(check_insertion_time_bloom(bloom_4, fileName))
    insertion_times.append(check_insertion_time_bloom(bloom_5, fileName))    
    insertion_times.append(check_insertion_time_bloom_simple(bloom_simple, fileName))
    insertion_times.append(check_insertion_time_cuckoo(cuckoo_filter, fileName))
    names = ["2DBF", "3DBF", "4DBF", "5DBF", "Simple Bloom", "Cuckoo"]

    plot_insertion_times(insertion_times, names)


"""
Different number of insertion time
"""
def check_different_number_of_insertion_time_bloom(filter, fileName, number_of_insertion):
    number_inserted = 0
    with open(fileName, mode="r") as book:
        start_time = time.time()
        for word in book.readlines():
            filter.setMember(word[:-1])
            number_inserted += 1
            if number_inserted == number_of_insertion:
                break
    end_time = time.time()
    return end_time - start_time


def check_different_number_of_insertion_time_bloom_simple(filter, fileName, number_of_insertion):
    number_inserted = 0
    with open(fileName, mode="r") as book:
        start_time = time.time()
        for word in book.readlines():
            filter.add(word[:-1])
            number_inserted += 1
            if number_inserted == number_of_insertion:
                break
    end_time = time.time()
    return end_time - start_time


def check_different_number_of_insertion_time_cuckoo(filter, fileName, number_of_insertion):
    number_inserted = 0
    with open(fileName, mode="r") as book:
        start_time = time.time()
        for word in book.readlines():
            filter.insert(word[:-1])
            number_inserted += 1
            if number_inserted == number_of_insertion:
                break
    end_time = time.time()
    return end_time - start_time


def compare_different_number_of_insertion_time():
    """
    Compare how much time it takes to insert 10, 100, 1000, etc. elemets for every filter on a given dataset.
    """
    bloom_2 = TwoDBF(31, 37, 4, print_info=False)
    bloom_3 = ThreeDBF(31, 37, 41, 4, print_info=False)
    bloom_4 = FourDBF(31, 37, 41, 43, 4, print_info=False)
    bloom_5 = FiveDBF(31, 37, 41, 43, 47, 4, print_info=False)
    bloom_simple = BloomFilter(max_elements=100000, error_rate=0.001)
    cuckoo_filter = CuckooFilter(capacity=100000, bucket_size=10000, fingerprint_size=1000)
    fileName = "DataCleaned3.txt"

    average_insertion_times = [0 for _ in range(19)]
    number_of_average = 100
    number_of_insertions = [5000, 10000, 15000, 20000, 25000, 30000, 35000, 40000, 45000, 50000, 55000, 60000, 65000, 70000, 75000, 80000, 85000, 90000, 95000]
    for a in range(number_of_average):
        print(a+1)
        insertion_times = []
        for i in number_of_insertions:
            insertion_times.append(check_different_number_of_insertion_time_bloom(bloom_2, fileName, i))
            #insertion_times.append(check_different_number_of_insertion_time_bloom(bloom_3, fileName, i))
            #insertion_times.append(check_different_number_of_insertion_time_bloom(bloom_4, fileName, i))
            #insertion_times.append(check_different_number_of_insertion_time_bloom(bloom_5, fileName, i))    
            #insertion_times.append(check_different_number_of_insertion_time_bloom_simple(bloom_simple, fileName, i))
            #insertion_times.append(check_different_number_of_insertion_time_cuckoo(cuckoo_filter, fileName, i))
        for i in range(len(insertion_times)):
            average_insertion_times[i] += insertion_times[i]/number_of_average
    names = ["2DBF"]    #, "3DBF", "4DBF", "5DBF", "Simple Bloom", "Cuckoo"]

    plot_different_number_of_insertion_times(average_insertion_times, names, number_of_insertions)


"""
Look up times
"""
def check_look_up_time_bloom(filter, fileName, number_of_look_up):
    with open(fileName, mode="r") as book:
        for word in book.readlines():
            filter.setMember(word[:-1])
    
    number_looked_up = 0
    with open(fileName, mode="r") as book:
        start_time = time.time()
        for word in book.readlines():
            filter.testMember(word[:-1])
            if number_looked_up == number_of_look_up:
                break
    end_time = time.time()
    return end_time - start_time


def check_look_up_time_bloom_simple(filter, fileName, number_of_look_up):
    with open(fileName, mode="r") as book:
        for word in book.readlines():
            filter.add(word[:-1])
    
    number_looked_up = 0
    with open(fileName, mode="r") as book:
        start_time = time.time()
        for word in book.readlines():
            assert word[:-1] in filter
            if number_looked_up == number_of_look_up:
                break
    end_time = time.time()
    return end_time - start_time


def check_look_up_time_cuckoo(filter, fileName, number_of_look_up):
    with open(fileName, mode="r") as book:
        for word in book.readlines():
            filter.insert(word[:-1])
    
    number_looked_up = 0
    with open(fileName, mode="r") as book:
        start_time = time.time()
        for word in book.readlines():
            filter.contains(word[:-1])
            if number_looked_up == number_of_look_up:
                break
    end_time = time.time()
    return end_time - start_time


def compare_look_up_times():
    """
    Compare how much time it takes to look up for a certain number of woorks for every filter on a given dataset.
    """
    bloom_2 = TwoDBF(31, 37, 4, print_info=False)
    bloom_3 = ThreeDBF(31, 37, 41, 4, print_info=False)
    bloom_4 = FourDBF(31, 37, 41, 43, 4, print_info=False)
    bloom_5 = FiveDBF(31, 37, 41, 43, 47, 4, print_info=False)
    bloom_simple = BloomFilter(max_elements=100000, error_rate=0.001)
    cuckoo_filter = CuckooFilter(capacity=100000, bucket_size=10000, fingerprint_size=1000)
    fileName = "DataCleaned3.txt"

    number_of_look_up = 10000
    look_up_times = []
    look_up_times.append(check_look_up_time_bloom(bloom_2, fileName, number_of_look_up))
    look_up_times.append(check_look_up_time_bloom(bloom_3, fileName, number_of_look_up))
    look_up_times.append(check_look_up_time_bloom(bloom_4, fileName, number_of_look_up))
    look_up_times.append(check_look_up_time_bloom(bloom_5, fileName, number_of_look_up))    
    look_up_times.append(check_look_up_time_bloom_simple(bloom_simple, fileName, number_of_look_up))
    look_up_times.append(check_look_up_time_cuckoo(cuckoo_filter, fileName, number_of_look_up))
    names = ["2DBF", "3DBF", "4DBF", "5DBF", "Simple Bloom", "Cuckoo"]

    plot_look_up_times(look_up_times, names)


"""
False positive probability
"""
def nCr(n, r):
    r = min(r, n-r)
    numer = reduce(op.mul, range(n, n-r, -1), 1)
    denom = reduce(op.mul, range(1, r+1), 1)
    return numer // denom  # or / in Python 2


def compute_false_positive_probability(sigma, alpha, X, Y):
    tau = (sigma//alpha)*X*Y
    n = 1000

    false_positive_probability = 0
    for i in range(tau):
        first_sum = (i/tau) * (tau, i)
        second_sum = 0
        for j in range(i):
            second_sum += (-1)**j * nCr(i, j) * ((i-j)/tau)**n
        false_positive_probability += first_sum * second_sum
    return false_positive_probability


if __name__ == "__main__":
    # compare_processing_times()
    # compare_insertion_time()
    # compare_different_number_of_insertion_time()
    # compare_look_up_times()
    fpp = compute_false_positive_probability(64, 4, 31, 37)
    print(fpp)
