"""
Kaede Yoshikawa
CSE 163 Final Project
This file contains code for the third research question: To what extent do social media trends influence how people
interact with mobile games? When run, it produces 1 image containing 6 graphs about the media trends, number of
installs, and the average review.
"""

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib


def plot_graphs(gp, gt):
    """
    Given two pandas DataFrames containing information on games from the Google Play Store, generates 1 image
    containing 6 plots pertaining to the media trend, number of installs, and the average review.
    :param gp: A pandas Dataframe containing the cleaned data from the Google Play Store
    :param gt: A pandas Dataframe containing the cleaned data from Google Trends
    :return: None
    """
    merged = gt.merge(gp, left_on="title", right_on="title")
    fig, axs = plt.subplots(2, 3, figsize=(8, 5))
    xs = ["upper_q", "mode", "st_dev"]
    ys = ["log_reviews", "log_installs"]
    for i, x in enumerate(xs):
        for j, y in enumerate(ys):
            sns.scatterplot(data=merged, x=x, y=y, ax=axs[j, i])
    plt.setp(axs[0, :], xticks=[])
    plt.setp(axs[:, 1:], yticks=[])
    plt.suptitle("Trend Values vs Popularity")
    plt.tight_layout()
    # plt.show()
    plt.savefig("plots/trend_analysis.png")


def main():
    matplotlib.use('TkAgg')  # Code to make matplotlib runnable in my computer
    gp = pd.read_csv("data/cleaned_google_play.csv")
    gt = pd.read_csv("data/google_trends.csv")
    plot_graphs(gp, gt)


if __name__ == "__main__":
    main()