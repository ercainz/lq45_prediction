import pandas as pd
import numpy as np
import pickle

class LoadRawData():
    def __init__(self, csv):
        self.csv = csv


    def __str__(self):
        return f"csv\t= {self.csv}"


    def __getrawdata_csv(self):
        defname = '__getrawdata_csv'
        try:
            return pd.read_csv(self.csv, parse_dates=['date'])
        except Exception as e:
            print(f"ERROR [{defname}] : {str(e)}")


    def __create_dataframe(self, pred_day):
        defname = '__create_dataframe'
        try:
            df = self.__getrawdata_csv().copy()
            df.set_index(['date'],inplace=True)

            target_list = ['STRONG SELL','SELL','HOLD','BUY','STRONG BUY']
            column_list = list(df.columns) + ['target','target_id']

            # lq45 changes: 4 days
            df[f'next_{pred_day}d'] = df.lq45.shift(-pred_day)
            df['changes'] = (df[f'next_{pred_day}d'] / df.lq45)-1

            df['target'] = np.where(df.changes < -0.03, target_list[0],
                                        np.where(df.changes < -0.01, target_list[1],
                                            np.where(df.changes > 0.03, target_list[4],
                                                np.where(df.changes > 0.01, target_list[3],
                                                    target_list[2]))))
            df['target'] = pd.Categorical(df.target, categories=target_list, ordered=False)
            df['target_id'] = pd.Categorical(df.target).codes - 2

            return df.loc[:, column_list]

        except Exception as e:
            print(f"ERROR [{defname}] : {str(e)}")


    def create_pkl(self, pkl):
        defname = 'create_pkl'
        try:
            with open(pkl, 'wb') as f:
                obj = self.__create_dataframe(pred_day=4)
                pickle.dump(obj, f)
                print(f'"{pkl}" has been created')

        except Exception as e:
            print(f"ERROR [{defname}] : {str(e)}")


    def load_pkl(self, pkl):
        defname = 'load_pkl'
        try:
            with open(pkl, 'rb') as f:
                return pickle.load(f)

        except Exception as e:
            print(f"ERROR [{defname}] : {str(e)}")
