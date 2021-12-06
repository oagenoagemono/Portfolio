"""
Kaede Yoshikawa
CSE 163 Final Project
This file contains code for the second research question: Are negative reviews worth considering in considering how
addictive a game is? When run, it produces 1 image containing 9 plots to analyze the Steam Store data
(https://www.kaggle.com/nikdavis/steam-store-games?select=steam.csv).
"""
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib
import numpy as np

FILE_NAME = "data/steam.csv"


def log_pt(playtime):
    """
    Takes a number playtime and returns the playtime in log base 10. Will return None if the value is 0.
    :param playtime: number indicating the play time
    :return: float indicating the play time in log base 10
    """
    if playtime != 0:
        return np.log10(playtime)


def get_df(file):
    """
    Takes a string path to a csv file, and returns a pandas DataFrame with unnecessary columns removed and additional
    columns needed for plotting calculated.
    :param file: String path to a file
    :return: pandas DataFrame containing the cleaned Steam Store data.
    """
    df = pd.read_csv(file)
    columns = ['positive_ratings', 'negative_ratings', 'average_playtime', 'median_playtime']
    df = df.loc[:, columns]
    df["percent_negative"] = df["negative_ratings"] / (df["positive_ratings"] + df["negative_ratings"])
    df["log_median"] = df["median_playtime"].apply(log_pt)
    df["log_mean"] = df["average_playtime"].apply(log_pt)
    df = df.dropna()
    df["log_ratio"] = df["log_mean"] - df["log_median"]
    return df


def plot_graphs(data):
    """
    Takes a pandas DataFrame containing the cleaned Steam Store data and generates a image containing 3 plots about
    the percentage of negativeratings and the playtime used for analysis of the Steam Store data and saves the image
    as "plots/steam_analysis.png".
    :param data: pandas DataFrame containing the cleaned Steam Store data.
    :return: None
    """
    fig, axs = plt.subplots(3, 2, figsize=(10, 8))
    ys = ['log_mean', 'log_median', "log_ratio"]
    for i, y in enumerate(ys):
        sns.scatterplot(data=data, x="percent_negative", y=y, ax=axs[i, 0])
        sns.kdeplot(data=data, x="percent_negative", y=y, ax=axs[i, 1], fill=True)
    plt.setp(axs[:2, :], xticks=[])
    plt.setp(axs[:, 1:], yticks=[])
    plt.suptitle("Percentage of Negative reviews vs Playtime on log scale")
    plt.tight_layout()
    # plt.show()
    plt.savefig("plots/steam_analysis.png")


def main():
    matplotlib.use('TkAgg')  # Code to make matplotlib runnable in my computer
    df = get_df(FILE_NAME)
    plot_graphs(df)


if __name__ == "__main__":
    main()