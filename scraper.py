import pandas as pd
import os

DIRECTORY_NAME = "dataset"
LISTING_FILENAME = "listings.csv"
REVIEWS_FILENAME = "reviews.csv"

if __name__ == "__main__":
    os.chdir(DIRECTORY_NAME)
    
    directoryList = os.listdir()
    for directory in directoryList:
        os.chdir(directory)

        listingDataFrame = pd.read_csv(LISTING_FILENAME)
        print("LISTING:")
        print(list(listingDataFrame.columns.values))
        print("====================\n\n")
        reviewsDataFrame = pd.read_csv(REVIEWS_FILENAME)
        print("REVIEWS:")
        print(list(reviewsDataFrame.columns.values))
        print("====================\n\n")


        os.chdir("..")
        break