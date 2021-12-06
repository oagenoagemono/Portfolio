# Instructions

## Imported Libraries 
* [pandas](https://pandas.pydata.org/pandas-docs/stable/getting_started/install.html)
* [matplotlib](https://matplotlib.org/stable/users/installing.html)
* [numpy](https://numpy.org/install/)
* [seaborn](https://seaborn.pydata.org/installing.html)
* [pytrends](https://pypi.org/project/pytrends/)
* [scikit-learn](https://scikit-learn.org/stable/install.html)

These libraries can be installed with pip or Anaconda. If more information is necessary, then visit their installation guide (hyperlinked).

## Downloaded Data
* [Google Play Store data](https://www.kaggle.com/dipanjandas96/play-store-game-reviews)
* [Steam Store data](https://www.kaggle.com/nikdavis/steam-store-games?select=steam.csv)

The download link to the datasets can be found at the top of the page. When downloaded, place them in a folder named _data_ in the same level as the python files. Do not change the names, for it will mess up the code.

## Running the Code
After the libraries are installed and the data is downloaded, simply run the provided code sequentially from _researchq_1.py_ to _researchq_4.py_. If there is an error from _researchq_3_1.py_ due to too many requests:
1. Comment out line 107 and either line 104 or 105 and run the code
2. If that succeeds, then run the other code
3. Comment out both line 104 and 105 and run line 107. 

If _researchq_1.py_ times out before producing a plot, try changing the argument in line 124 to:
* GTKAgg
* GTK3Agg
* GTKCairo
* GTK3Cairo
* WXAgg
* Qt4Agg
* Qt5Agg

If the arguments presented above do not work, consult the [matplotlib FAQ page](https://matplotlib.org/2.0.2/faq/usage_faq.html#wx-backends) for more information on the backends, or simply check if matplotlib is installed.

After running the code, the plots produced should be found under a folder named _plots_ as a png image. The results for _researchq_4.py_ will be printed to the terminal.