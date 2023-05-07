import datetime
import json
import math

import seaborn as sns
import matplotlib.pyplot as plt

from matplotlib.colors import LogNorm
from pandas import DataFrame
from dateutil.relativedelta import relativedelta

dataframe = DataFrame()


def read_dictionary(filename):
    userdict = {}
    with open(filename, encoding="utf8") as json_file:
        data = json.load(json_file)
        for key in data.keys():
            userdict[key] = data[key]
        return userdict


def read_file(file, gapless=True, use_dictionary=False):
    if use_dictionary:
        userdict = read_dictionary('../dictionary.json')

    with open(file, encoding="utf8") as json_file:
        data = json.load(json_file)

        if gapless:
            start_date = datetime.datetime.strptime(data['messages'][0]['date'], "%Y-%m-%dT%H:%M:%S")
            while start_date <= datetime.datetime.today():
                dataframe[start_date.strftime('%Y-%m')] = 0
                start_date += relativedelta(months=1)

        for p in data['messages']:

            if p['type'] == 'message':
                date = datetime.datetime.strptime(p['date'], "%Y-%m-%dT%H:%M:%S").strftime('%Y-%m')

                if use_dictionary:
                    user_from = userdict[p['from_id']]
                else:
                    user_from = p['from']

                if user_from is None:
                    user_from = p['from_id']

                # If previous members of your chat have deleted their accounts, p['from'] will be None.
                # Therefore it is replaced here with their 'from_id'.
                # You can use a { from-id : username } dictionary to translate ids to usernames, and restore
                # missing names manually from context.

                #   ----> see create_dictionary.py for more <----

                previous = 0
                previous_total = 0

                #  in case cell does not exist yet (index or column not created)
                try:
                    previous_total = dataframe.at[str(user_from), 'total']
                    previous = dataframe.at[str(user_from), date]
                except:
                    pass

                # NaN in case cell has not been written to
                if math.isnan(previous):
                    previous = 0
                if math.isnan(previous_total):
                    previous_total = 0

                dataframe.at[str(user_from), date] = previous + 1
                dataframe.at[str(user_from), 'total'] = previous_total + 1


def process_file(sort=True):
    global dataframe

    # fill empty dataframe entries with 0
    dataframe.fillna(0, inplace=True)

    if sort:
        dataframe = dataframe.sort_values(by='total', ascending=False)

    print(dataframe['total'])
    dataframe.drop(columns='total', inplace=True)

    # add offset because 0 doesn't appear on log scale
    dataframe += 1


def draw_map(x=20, y=10):
    plt.subplots(figsize=(x, y))
    sns.heatmap(dataframe, annot=False, norm=LogNorm())
    plt.show()


if __name__ == "__main__":
    read_file('../demodata.json', gapless=True, use_dictionary=False)
    process_file(sort=True)
    draw_map(15, 40)
