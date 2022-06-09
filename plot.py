import matplotlib.pyplot as plt
import numpy as np


def plot_processing_times(processing_times, names):
    plt.bar(np.arange(len(processing_times)), processing_times, tick_label=names, color=["k", "r", "b", "g", "y", "c"])
    plt.ylabel("Processing time in seconds")
    plt.title("Processing time on the 3rd dataset")
    plt.show()


def plot_insertion_times(insertion_times, names):
    plt.bar(np.arange(len(insertion_times)), insertion_times, tick_label=names, color=["k", "r", "b", "g", "y", "c"])
    plt.ylabel("Time taken to process one key in seconds")
    plt.title("Insertion time per key on the 3rd dataset")
    plt.show()


def plot_different_number_of_insertion_times(insertion_times, names, number_of_insertion):
    insertion_times_sorted = []
    names_complete = []
    for i in range(len(names)):
        for j in range(len(number_of_insertion)):
            insertion_times_sorted.append(insertion_times[j*len(names) + i])
            names_complete.append(names[i] + "-" + str(number_of_insertion[j]))
    # plt.bar(np.arange(len(insertion_times_sorted)), insertion_times_sorted)
    plt.plot(np.arange(len(insertion_times_sorted)), insertion_times_sorted)
    plt.xticks(np.arange(len(insertion_times_sorted)), labels=names_complete, rotation=90)
    plt.ylabel("Time taken to process the keys in seconds")
    plt.title("Time taken to precess different number of keys for 2DBF on the 3rd dataset")
    plt.show()


def plot_look_up_times(look_up_times, names):
    plt.bar(np.arange(len(look_up_times)), look_up_times, tick_label=names, color=["k", "r", "b", "g", "y", "c"])
    plt.ylabel("Time taken to look up 10000 keys in seconds")
    plt.title("Look up time on the 3rd dataset")
    plt.show()
