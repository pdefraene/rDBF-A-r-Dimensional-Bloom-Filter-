import time
import random

from cuckoopy import CuckooFilter
from bloom_filter import BloomFilter

from TwoDBF import TwoDBF
from ThreeDBF import ThreeDBF
from FourDBF import FourDBF
from FiveDBF import FiveDBF

from plot import *



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

def compare_processing_time(fileName = "DataCleaned3.txt"):
    """
    Compare the total processing time taken by all filters on a given dataset.
    """
    bloom_2 = TwoDBF(31, 37, 4, print_info=False)
    bloom_3 = ThreeDBF(31, 37, 41, 4, print_info=False)
    bloom_4 = FourDBF(31, 37, 41, 43, 4, print_info=False)
    bloom_5 = FiveDBF(31, 37, 41, 43, 47, 4, print_info=False)
    bloom_simple = BloomFilter(max_elements=100000, error_rate=0.001)
    cuckoo_filter = CuckooFilter(capacity=100000, bucket_size=10000, fingerprint_size=1000)
    
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

def compare_insertion_time(fileName="DataCleaned3.txt"):
    """
    Compare how much time every insertion takes for every filter on a given dataset.
    """
    bloom_2 = TwoDBF(31, 37, 4, print_info=False)
    bloom_3 = ThreeDBF(31, 37, 41, 4, print_info=False)
    bloom_4 = FourDBF(31, 37, 41, 43, 4, print_info=False)
    bloom_5 = FiveDBF(31, 37, 41, 43, 47, 4, print_info=False)
    bloom_simple = BloomFilter(max_elements=100000, error_rate=0.001)
    cuckoo_filter = CuckooFilter(capacity=100000, bucket_size=10000, fingerprint_size=1000)

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
Different Number of Insertion Time
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

def compare_different_number_of_insertion_time(fileName = "DataCleaned3.txt"):
    """
    Compare how much time it takes to insert 5000, 10000, 15000, etc. elemets for every filter on a given dataset.
    """
    bloom_2 = TwoDBF(31, 37, 4, print_info=False)
    bloom_3 = ThreeDBF(31, 37, 41, 4, print_info=False)
    bloom_4 = FourDBF(31, 37, 41, 43, 4, print_info=False)
    bloom_5 = FiveDBF(31, 37, 41, 43, 47, 4, print_info=False)
    bloom_simple = BloomFilter(max_elements=100000, error_rate=0.001)
    cuckoo_filter = CuckooFilter(capacity=1000000, bucket_size=100000, fingerprint_size=10000)

    number_of_insertions = [5000, 10000, 15000, 20000, 25000, 30000, 35000, 40000, 45000, 50000, 55000, 60000, 65000, 70000, 75000, 80000, 85000, 90000, 95000]
    insertion_times = []
    for i in number_of_insertions:
        insertion_times.append(check_different_number_of_insertion_time_bloom(bloom_2, fileName, i))
        insertion_times.append(check_different_number_of_insertion_time_bloom(bloom_3, fileName, i))
        insertion_times.append(check_different_number_of_insertion_time_bloom(bloom_4, fileName, i))
        insertion_times.append(check_different_number_of_insertion_time_bloom(bloom_5, fileName, i))    
        insertion_times.append(check_different_number_of_insertion_time_bloom_simple(bloom_simple, fileName, i))
        insertion_times.append(check_different_number_of_insertion_time_cuckoo(cuckoo_filter, fileName, i))

    names = ["2DBF", "3DBF", "4DBF", "5DBF", "Simple Bloom", "Cuckoo"]
    plot_different_number_of_insertion_times(insertion_times, names, number_of_insertions)



"""
Look Up Times
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

def compare_look_up_times(fileName="DataCleaned3.txt", number_of_look_up=10000):
    """
    Compare how much time it takes to look up for a certain number of woorks for every filter on a given dataset.
    """
    bloom_2 = TwoDBF(31, 37, 4, print_info=False)
    bloom_3 = ThreeDBF(31, 37, 41, 4, print_info=False)
    bloom_4 = FourDBF(31, 37, 41, 43, 4, print_info=False)
    bloom_5 = FiveDBF(31, 37, 41, 43, 47, 4, print_info=False)
    bloom_simple = BloomFilter(max_elements=100000, error_rate=0.001)
    cuckoo_filter = CuckooFilter(capacity=100000, bucket_size=10000, fingerprint_size=1000)

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
False Positive
"""
def random_string_of_chars(length):
    letters = "qwertyuiopasdfghjklzxcvbnm"
    return "".join((random.choice(letters) for i in range(length)))

def compute_false_positive(bloom, number_of_insert, number_of_trials):
    for _ in range(number_of_insert):
        bloom.setMember(random_string_of_chars(100))
    false_positive = 0
    for _ in range(number_of_trials):
        random_word = random_string_of_chars(100)   
        if bloom.testMember(random_word):
            false_positive += 1
    return 100*false_positive/number_of_trials

def compare_false_positive(trials=100):
    """
    Compare the false positive rate for each filter, for random words of length 100.
    The comparison is made on 2000 insertions and 1000 look ups.
    """
    all_res_2 = 0
    all_res_3 = 0
    all_res_4 = 0
    all_res_5 = 0

    for i in range(trials):
        print(i+1)
        bloom_2 = TwoDBF(31, 37, 4, print_info=False)
        bloom_3 = ThreeDBF(31, 37, 2, 4, print_info=False)
        bloom_4 = FourDBF(31, 37, 2, 3, 4, print_info=False)
        bloom_5 = FiveDBF(31, 37, 2, 3, 5, 4, print_info=False)
        all_res_2 += compute_false_positive(bloom_2, 2000, 1000)
        all_res_3 += compute_false_positive(bloom_3, 2000, 1000)
        all_res_4 += compute_false_positive(bloom_4, 2000, 1000)
        all_res_5 += compute_false_positive(bloom_5, 2000, 1000)

    print(f"bloom 2 : {round(all_res_2/trials, 3)} %")
    print(f"bloom 3 : {round(all_res_3/trials, 3)} %")
    print(f"bloom 4 : {round(all_res_4/trials, 3)} %")
    print(f"bloom 5 : {round(all_res_5/trials, 3)} %")
