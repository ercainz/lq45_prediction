import pandas as pd

def load_csv(csv_name):
    defname = 'read_data|load_csv'
    try:
        df = pd.read_csv(csv_name, parse_dates=['date'])
        df.set_index(['date'],inplace=True)
        return df
    except Exception as e:
        print(f"ERROR [{defname}] : {str(e)}")
#==========================================================================================================================#
#==========================================================================================================================#


'''
def __create_dataframe(df, pred_day):
    defname = '__create_dataframe'
    try:
        df = self.load_csv().copy()

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
'''

