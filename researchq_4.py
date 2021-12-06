"""
Kaede Yoshikawa
CSE 163 Final Project
This file contains code for the fourth research question: Is a new mobile game with certain features going to get a good rating? When run, it prints the result of the train and test evaluations.
"""

import pandas as pd
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split


def machine_learning(data):
    """"""
    filtered = data.loc[:, ["score", 'overall_price', 'size', 'genre', 'contentRating', 'containsAds']]
    filtered = filtered.dropna()
    columns = ['overall_price', 'size', 'genre', 'contentRating', 'containsAds']
    labels = filtered["score"]
    features = filtered.loc[:, columns]
    features = pd.get_dummies(features)
    trials = 10
    tests = list()
    trains = list()
    for i in range(trials):
        features_train, features_test, labels_train, labels_test = \
            train_test_split(features, labels, test_size=0.25)
        model = DecisionTreeRegressor(max_depth=5)
        model.fit(features_train, labels_train)
        test_label_predictions = model.predict(features_test)
        train_label_predictions = model.predict(features_train)
        test_acc = mean_squared_error(labels_test, test_label_predictions)
        train_acc = mean_squared_error(labels_train, train_label_predictions)
        tests.append(test_acc)
        trains.append(train_acc)
    print("Average test error: ", sum(tests) / trials)
    print("Average train error: ", sum(trains) / trials)
    # Average test error: 0.1639596375229368
    # Average train error: 0.061694513334370996


def main():
    data = pd.read_csv("data/cleaned_google_play.csv")
    machine_learning(data)


if __name__ == "__main__":
    main()