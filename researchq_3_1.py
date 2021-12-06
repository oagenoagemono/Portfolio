"""
Kaede Yoshikawa
CSE 163 Final Project
This file contains preparation code for the third research question: To what extent do social media trends influence
how people interact with mobile games? When run, it produces 3 csv files containing trend data for the games in the
Google Play Store data from Google Trends, obtained via pytrends.
"""

import pandas as pd
from pytrends.request import TrendReq
import statistics
import numpy as np


def query_gt(titles, filename):
    """
    Given a list of game titles and saves half of the trend data for all of the games as a csv file with
    the given filename as its file name.
    :param titles: A string list of game titles
    :param filename: A string file name to save the information
    :return:
    """
    res = pd.DataFrame(titles, columns=["title"])
    trend = list()
    for kw in titles:
        pytrends = TrendReq(hl='en-US', tz=360)
        pytrends.build_payload(kw_list=[kw], timeframe="today 5-y")
        iot = pytrends.interest_over_time()
        if not iot.empty:
            nums = iot[kw].tolist()
        else:
            nums = list()
        trend.append(nums)
    res["trend"] = pd.Series(trend)
    res.to_csv(filename, index=False)


def clean_df(paths):
    """
    Takes a string list of paths to csv files containing game titles and their trend data and saves the cleaned
    DataFrame as a csv file named "data/google_trends.csv" for use in researchq_3_2.py.
    :param paths: A list of strings containing the paths to the obtained Google Trends data.
    :return: None
    """
    d0 = pd.read_csv(paths[0])
    d1 = pd.read_csv(paths[1])
    df = pd.concat([d0, d1], ignore_index=True)
    df["trend"] = df["trend"].apply(clean_list)
    df = df[df["trend"].notna()]
    df = df[df["title"].notna()]
    df["upper_q"] = df["trend"].apply(upper_quartile)
    df["mode"] = df["trend"].apply(calc_mode)
    df["st_dev"] = df["trend"].apply(st_dev)
    df.to_csv("data/google_trends.csv", index=False)


def clean_list(li):
    """
    Given a list, removes all values that are not numbers. If the list is empty, returns an empty list.
    :param li: list of numbers and other values
    :return: list of numbers
    """
    li = li[1:-1]
    if len(li) != 0:
        li = li.split(", ")
        return [float(item) for item in li]


def upper_quartile(num_list):
    """
    Given a list of numbers indicating the trend, returns the Q3 (75 percentile). If the list is empty, returns
    None.
    :param num_list: list of integer numbers
    :return: float value of Q3 or None
    """
    if len(num_list) != 0:
        return np.percentile(num_list, 75)


def calc_mode(num_list):
    """
    Given a list of numbers indicating the trend, returns the mode. If the list is empty, returns None.
    :param num_list: list of integer numbers
    :return: float value of mode or None
    """
    if len(num_list) != 0:
        return statistics.mode(num_list)


def st_dev(num_list):
    """
    Given a list of numbers indicating the trend, returns the standard deviation. If the list is empty, returns
    None.
    :param num_list: list of integer numbers
    :return: float value of mode or None
    """
    if len(num_list) != 0:
        return np.std(num_list)


def main():
    df = pd.read_csv("data/cleaned_google_play.csv")
    keywords = df["title"].tolist()
    query_gt(keywords[:(len(keywords) // 2)], "data/google_trends_1.csv")
    query_gt(keywords[(len(keywords) // 2):], "data/google_trends_2.csv")
    paths = ["data/google_trends_1.csv", "data/google_trends_2.csv"]
    clean_df(paths)


if __name__ == "__main__":
    main()