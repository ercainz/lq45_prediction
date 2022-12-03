import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import joblib
import configparser

def read_config(config_dir, section, key):
    defname = 'global_func|read_config'
    try:
        cfg = configparser.ConfigParser()    
        cfg.read(f'{config_dir}config.ini')

        return cfg[section][key]
    except Exception as e:
        print(f"ERROR [{defname}] : {str(e)}")
#==========================================================================================================================#
#==========================================================================================================================#
def save_as_pkl(obj, filename, compress=3):
    '''
    compress :\n
        int from 0 to 9.\n
        Optional compression level for the data.\n
        0 is no compression. Higher value means more compression, but also slower read and write times.\n
        Using a value of 3 is often a good compromise.\n
    '''
    defname = 'global_func|save_as_pkl'
    try:
        joblib.dump(obj, filename=filename, compress=compress)
    except Exception as e:
        print(f"ERROR [{defname}] : {str(e)}")
#==========================================================================================================================#
#==========================================================================================================================#
def load_from_pkl(filename):
    defname = 'global_func|load_from_pkl'
    try:
        obj = joblib.load(filename=filename)
        return obj
    except Exception as e:
        print(f"ERROR [{defname}] : {str(e)}")
#==========================================================================================================================#
#==========================================================================================================================#
def api_homepage():
    defname = 'global_func|api_homepage'
    try:
        config_dir = 'config\\'
        dict_result = {"Name": read_config(config_dir=config_dir, section='PROJECT', key='NAME'),
                        "Description": read_config(config_dir=config_dir, section='PROJECT', key='DESCRIPTION'),
                        "Author": read_config(config_dir=config_dir, section='PROJECT', key='AUTHOR'),
                        "Version": read_config(config_dir=config_dir, section='PROJECT', key='VERSION'),
                        "Last Update": read_config(config_dir=config_dir, section='PROJECT', key='LASTUPDATE'),
                        "Documentation": read_config(config_dir=config_dir, section='PROJECT', key='DOCS'),
                        }

        return dict_result
    except Exception as e:
        print(f"ERROR [{defname}] : {str(e)}")
#==========================================================================================================================#
#==========================================================================================================================#
def plotting_hist_all(dataframe, savefig=''):
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

    if savefig != '':
        fig.savefig(savefig)
#==========================================================================================================================#
#==========================================================================================================================#
def plotting_line_all(dataframe, savefig=''):
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

    if savefig != '':
        fig.savefig(savefig)
#==========================================================================================================================#
#==========================================================================================================================#
def plotting_box_all(dataframe, savefig=''):
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

    if savefig != '':
        fig.savefig(savefig)
#==========================================================================================================================#
#==========================================================================================================================#
