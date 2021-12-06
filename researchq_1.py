"""
Kaede Yoshikawa
CSE 163 Final Project
This file contains code for the first research question: Which features of a mobile app correlate to the average rating?
When run, it produces 1 csv file containing a cleaned version of the Google Play Store data
(https://www.kaggle.com/dipanjandas96/play-store-game-reviews) for analysis and 4 images containing 6 plots each to
analyze the Google Play Store data.
"""
import pandas as pd
import json
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib
import numpy as np

FILE_NAME = "data/PlayStoreGameAppInfoReview.json"


def str_list_to_average(str_list):
    """
    Helper function that takes a list of strings and returns the average value in float.
    If the value is None, then returns 0.0
    :param str_list: list of strings representing numbers
    :return: float value of the calculated average value
    """
    if str_list is not None:
        return np.mean([float(item) for item in str_list])
    else:
        return 0.0


def get_min_histogram(num_list):
    """
    Helper function that takes a list of integers and returns the first index, which indicates the number of ratings
    with a rating of 1. If the game does not have a histogram, will return None.
    :param num_list: list of numbers representing the number of ratings
    :return: integer value of the number of 1-star ratings
    """
    if num_list is not None:
        return num_list[0]


def get_max_histogram(num_list):
    """
    Helper function that takes a list of integers and returns the last index, which indicates the number of ratings
    with a rating of 5. If the game does not have a histogram, will return None.
    :param num_list: list of numbers representing the number of ratings
    :return: integer value of the number of 5-star ratings
    """
    if num_list is not None:
        return num_list[-1]


def clean_json(path):
    """
    Takes a path to a JSON file containing the Google Play Store data as a sting and returns and saves the new DataFrame
    as a csv file named "data/cleaned_google_play.csv".
    :param path: string path to a JSON file containing the Google Play Store data
    :return: a cleaned pandas DataFrame of the Google Play Store data
    """
    file_name = "data/cleaned_google_play.csv"
    with open(path) as f:
        data_json = json.load(f)
        data_json = [data_json[key]["appInfo"] for key in data_json.keys()]
        data = pd.json_normalize(data_json)
        columns = ['title', 'minInstalls', 'score', 'ratings', 'reviews', 'price', 'inAppProductPrice',
                   'size', 'genre', 'contentRating', 'containsAds']
        histogram = data["histogram"].copy()
        data = data.loc[:, columns]
        data[data["size"] == "Varies with device"] = None
        size_int = pd.to_numeric(data.loc[data["size"].notnull(), "size"].str.replace("M", "", case=False))
        data.loc[data["size"].notnull(), "size"] = size_int
        iap_range = data["inAppProductPrice"].str.findall("\d+\.\d+")
        iap_range = iap_range.apply(str_list_to_average)
        data["inAppProductPrice"] = iap_range
        data["log_reviews"] = np.log(data["reviews"])
        data["log_installs"] = np.log(data["minInstalls"])
        data["review_1"] = histogram.apply(get_min_histogram) / data["ratings"]
        data["review_5"] = histogram.apply(get_max_histogram) / data["ratings"]
        data["overall_price"] = iap_range * 0.05 + data["price"]
        data.to_csv(file_name, index=False)
        return data


def plot_graphs(data):
    """
    Generates 4 images containing 6 graphs each in the plots folder used for analysis of the Google Play Store Data.
    :param data: a cleaned pandas DataFrame of the Google Play Store data
    :return: None
    """
    titles = ["Game Data vs Average Rating", "Game Data vs Percentage of 1-star Reviews",
              "Game Data vs Percentage of 5-star Reviews"]
    ys = ["score", "review_1", "review_5"]
    names = ["plots/scatter_avg.png", "plots/scatter_1s.png", "plots/scatter_5s.png"]
    for i in range(3):
        fig, axs = plt.subplots(2, 3, figsize=(15, 10))
        sns.scatterplot(data=data, x="log_installs", y=ys[i], ax=axs[0, 0])
        sns.scatterplot(data=data, x="log_reviews", y=ys[i], ax=axs[0, 1])
        sns.scatterplot(data=data, x="inAppProductPrice", y=ys[i], ax=axs[0, 2])
        sns.scatterplot(data=data, x="size", y=ys[i], ax=axs[1, 0])
        sns.scatterplot(data=data, x="price", y=ys[i], ax=axs[1, 1])
        sns.scatterplot(data=data, x="overall_price", y=ys[i], hue="containsAds", ax=axs[1, 2])
        plt.suptitle(titles[i])
        plt.savefig(names[i])
        # plt.show()
    fig, axs = plt.subplots(3, 2, figsize=(8, 8))
    for i in range(3):
        sub_genre = data.loc[:, ["genre", ys[i]]].groupby("genre").mean()
        sub_genre = sub_genre.reset_index()
        sub_content = data.loc[:, ["contentRating", ys[i]]].groupby("contentRating").mean()
        sub_content = sub_content.reset_index()
        plt.setp(axs[i, 0].xaxis.get_majorticklabels(), rotation=90, fontsize='x-small')
        plt.setp(axs[i, 1].xaxis.get_majorticklabels(), rotation=30, fontsize='x-small')
        sns.barplot(data=sub_genre, x="genre", y=ys[i], ax=axs[i, 0], color="c")
        sns.barplot(data=sub_content, x="contentRating", y=ys[i], ax=axs[i, 1], color="c")
    plt.setp(axs[:2, :], xticks=[])
    plt.suptitle("Game Categories vs Ratings")
    plt.tight_layout()
    plt.savefig("plots/bar_rating.png")
    # plt.show()


def main():
    matplotlib.use('TkAgg')  # Code to make matplotlib runnable in my computer
    data = clean_json(FILE_NAME)
    plot_graphs(data)


if __name__ == "__main__":
    main()