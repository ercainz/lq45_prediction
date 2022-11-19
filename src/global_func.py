import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pickle

def create_pkl(obj, pkl):
    defname = 'global_func|create_pkl'
    try:
        with open(pkl, 'wb') as f:
            pickle.dump(obj, f)
            print(f'"{pkl}" ({type(obj)}) has been created')

    except Exception as e:
        print(f"ERROR [{defname}] : {str(e)}")
#==========================================================================================================================#
#==========================================================================================================================#
def load_pkl(pkl):
    defname = 'global_func|load_pkl'
    try:
        with open(pkl, 'rb') as f:
            return pickle.load(f)

    except Exception as e:
        print(f"ERROR [{defname}] : {str(e)}")
#==========================================================================================================================#
#==========================================================================================================================#
def plotting_hist_all(dataframe):
    fig, axes = plt.subplots(nrows=7
                            ,ncols=2
                            ,figsize=[16,20]
                            ,dpi=144
                            )

    for i,ax in enumerate(axes.flatten()):
        try:
            if i >= len(dataframe.columns):
                pass
            else:
                ax.set_title(f'{dataframe.columns[i].upper()}')
                sns.histplot(data=dataframe, x=dataframe.columns[i], ax=ax, kde=True, bins=100, stat='density', color=sns.color_palette()[4])
                ax.axvline(x=dataframe[dataframe.columns[i]].mean(),color='red',ls='-',label='mean')
                ax.axvline(x=dataframe[dataframe.columns[i]].median(),color='green',ls='-',label='median')
                ax.set_xlabel('')
                ax.legend(fontsize=10)
        except Exception as e:
            print(f"ERROR : {str(e)}")

    plt.tight_layout()
    plt.show(block=False)
#==========================================================================================================================#
#==========================================================================================================================#
def plotting_line_all(dataframe):
    fig, axes = plt.subplots(nrows=7
                            ,ncols=2
                            ,figsize=[16,20]
                            ,dpi=144
                            )

    for i,ax in enumerate(axes.flatten()):
        try:
            if i >= len(dataframe.columns):
                pass
            else:
                ax.set_title(f'{dataframe.columns[i].upper()}')
                sns.lineplot(data=dataframe, x=dataframe.index, y=dataframe.columns[i], ax=ax, color=sns.color_palette()[i % 10])
                ax.set_xlabel('')
        except Exception as e:
            print(f"ERROR : {str(e)}")

    plt.tight_layout()
    plt.show(block=False)
#==========================================================================================================================#
#==========================================================================================================================#
def plotting_box_all(dataframe):
    fig, axes = plt.subplots(nrows=7
                            ,ncols=2
                            ,figsize=[16,20]
                            ,dpi=144
                            )

    for i,ax in enumerate(axes.flatten()):
        try:
            if i >= len(dataframe.columns):
                pass
            else:
                ax.set_title(f'{dataframe.columns[i].upper()}')
                sns.boxplot(data=dataframe, x=dataframe.columns[i], ax=ax, flierprops={"marker": "x"}, color=sns.color_palette()[4])
                ax.set_xlabel('')
        except Exception as e:
            print(f"ERROR : {str(e)}")

    plt.tight_layout()
    plt.show(block=False)
#==========================================================================================================================#
#==========================================================================================================================#
