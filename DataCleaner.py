# link to find the book http://www.fullbooks.com/The-Shadow-of-the-North1.html

def cleanData(fileName):
    """
    Clean the data from the book to only have the interesting words.
    """
    newFile = open("DataCleaned3.txt", "w")
    with open(fileName, mode="r") as book:
        for i in book.readlines():
            line = i.split(" ")
            for word in line:
                word = word.strip()
                word = "".join(item for item in word if item.isalnum())
                if word.isalnum():
                    newFile.write(word.lower() + "\n")
    newFile.close()
    
if __name__ == "__main__":
    cleanData("dataBook.txt")
