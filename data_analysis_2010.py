import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns
import os

import argparse

def import_dataframe(filename):
    df = pd.read_csv(filename)
    df = df.drop('Unnamed: 0', axis = 1)

    total_exp = len(df[df.condition == 'expected'])
    total_mental = len(df[df.state == 'mental'])

    for trial in range(len(df)):
        timeout_count = 0
        if (df.loc[trial, 'response_time']=='timeout') == True:
            df.loc[trial, 'response_time'] = np.nan
            timeout_count += 1

    if df.response.dtype == 'O':
        df = df[df.response != 'timeout']
        df.response = pd.to_numeric(df.response)
        df.response_time = pd.to_numeric(df.response_time)

    df = df[['trial_num','state','condition','story_start','quest_start','time_of_response','response_time',
         'response']]
    return df, timeout_count, total_mental, total_exp

def split_trials_and_means(df):
    mental_exp = []
    mental_unexp = []
    physical_exp = []
    physical_unexp = []

    for trial in range(len(df)):
        if df['state'].iloc[trial] == 'mental':
            if df.condition.iloc[trial] == 'expected':
                mental_exp.append((df.response_time.iloc[trial], df.response.iloc[trial]))
            else:
                mental_unexp.append((df.response_time.iloc[trial], df.response.iloc[trial]))
        else:
            if df.condition.iloc[trial] == 'expected':
                physical_exp.append((df.response_time.iloc[trial], df.response.iloc[trial]))
            else:
                physical_unexp.append((df.response_time.iloc[trial], df.response.iloc[trial]))

    try:
        expected_rt = {'mental':np.mean([k for (k, v) in mental_exp]), 'physical': np.mean([k for (k, v) in physical_exp])}
        unexpected_rt = {'mental':np.mean([k for (k, v) in mental_unexp]), 'physical': np.mean([k for (k, v) in physical_unexp])}

        expected_resp = {'mental':np.mean([v for (k, v) in mental_exp]), 'physical': np.mean([v for (k, v) in physical_exp])}
        unexpected_resp = {'mental':np.mean([v for (k, v) in mental_unexp]), 'physical': np.mean([v for (k, v) in physical_unexp])}

        df_rt = pd.DataFrame({'expected_rt':expected_rt, 'unexpected_rt': unexpected_rt})
        df_resp = pd.DataFrame({'expected_resp': expected_resp, 'unexpected_resp': unexpected_resp})

        dfs = [df_rt, df_resp]

    except IndexError:
        dfs = ":-("
        print("Participant did not complete enough trials to analyze trends.")


    return dfs

def plotting_rt_resps(dfs, timeout_count, total_mental, total_exp, file):

    if not os.path.exists('data/images'):
        os.makedirs('data/images')

    if dfs != ":-(":
        for df in dfs:
            fig, ax = plt.subplots()

            width = 1

            ax1 = ax.bar(1, df.iloc[0,0], width, color = 'r')
            ax2 = ax.bar(2, df.iloc[1,0], width, color = 'b')

            ax1 = ax.bar(4, df.iloc[0,1], width, color = 'r')
            ax2 = ax.bar(5, df.iloc[1,1], width, color = 'b')

            ax.set_xticks((2, 5))
            ax.set_xlim(0, 7)
            ax.set_xticklabels(('Expected', 'Unexpected'))
            ax.legend((ax1[0], ax2[0]), ('Mental', 'Physical'))
            ax.set_ylim(0, 5)
            ax.text(0, 1, 'Timeouts = %s\nMental Trials = %s\nExpected Trials = %s' %
                                (timeout_count, total_mental, total_exp), fontsize=12, transform=ax.transAxes)
            if df.columns.any() == 'expected_rt':
                ax.set_ylabel('Response Times')
                ax.set_title('RT by condition and state')
                image_0 = file.replace("data/ToM_Task_2010", "data/images/Image")
                image = image_0.replace(".csv", "_1.png")
                plt.savefig(image)
            else:
                ax.set_ylabel('Responses')
                ax.set_title('Response scores by condition and state')
                image_0 = file.replace("data/ToM_Task_2010", "data/images/Image")
                image = image_0.replace(".csv", "_2.png")
                plt.savefig(image)
    else:
        print(dfs)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description = "Make images comparing ToM task resp and RT")
    parser.add_argument(nargs='+', dest='files',
                        help="Files from which to produce images"
                        )

    args = parser.parse_args()

    for file in args.files:
        if file.endswith('.csv'):
            df, timeout_count, total_mental, total_exp = import_dataframe(file)
            dfs = split_trials_and_means(df)
            plotting_rt_resps(dfs, timeout_count, total_mental, total_exp, file)
