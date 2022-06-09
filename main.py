from Analysis import compare_processing_time, compare_insertion_time, compare_different_number_of_insertion_time, \
    compare_look_up_times, compare_false_positive
from FalseNegativeProof import ProofFalseNegative


def main():
    """
    This will launch all the different comparisons used for the analysis.
    Some of them can take some time due to the number of trials used to make averages.
    Some parameters can be changed.

    3 datasets are available, "DataCleaned.txt", "DataCleaned2.txt" and "DataCleaned3.txt".
    Those datasets are composed of words taken from a book available online.
    Each word of the book has been extracted and cleaned (put to lowercase, ponctuation removed, etc.)
    This cleaning has been done in the "DataCleaner.py" file.
    """
    fileName = "DataCleaned3.txt"

    print("Processing time")
    compare_processing_time(fileName)
    print("Insertion time")
    compare_insertion_time(fileName)
    print("Different number of insertion time")
    compare_different_number_of_insertion_time(fileName)
    print("Look up time")
    compare_look_up_times(fileName, number_of_look_up=10000)
    print("False positive")
    compare_false_positive(trials=100)
    print("False negative proof")
    ProofFalseNegative()


if __name__ == "__main__":
    main()
