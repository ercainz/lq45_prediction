import pandas as pd
import numpy as np
import pickle

class DataPreprocessing():
    def __init__(self, dataframe):
        self.df = dataframe


    def resampling(self, interval='M'):
        '''
        interval :
            D   : calendar day frequency
            B   : business day frequency
            W   : weekly frequency
            MS  : month start frequency
            M   : month end frequency
            SMS : semi-month start frequency (1st and 15th)
            SM  : semi-month end frequency (15th and end of month)
            QS  : quarter start frequency
            Q   : quarter end frequency
            A   : year end frequency
            AS  : year start frequency
        '''
        defname = 'resampling'
        try:
            df = self.df.resample(interval).mean().fillna(method="ffill").copy()
            return df
        except Exception as e:
            print(f"ERROR [{defname}] : {str(e)}")


    def enriching(self):
        defname = 'enriching'
        try:
            df = self.df.copy()
            df['dom_total'] = df['dom_b'] + df['dom_s']
            df['dom_net'] = df['dom_b'] - df['dom_s']
            df['for_total'] = df['for_b'] + df['for_s']
            df['for_net'] = df['for_b'] - df['for_s']

            return df
        except Exception as e:
            print(f"ERROR [{defname}] : {str(e)}")


    def set_target(self, datacolumn='lq45', future_days=4):
        defname = 'set_target'
        try:
            df = self.df.copy()
            df['target'] = df[datacolumn].shift(-1*future_days)
            return df
        except Exception as e:
            print(f"ERROR [{defname}] : {str(e)}")


    def outlier_treatment(self, datacolumn, input_value):
        defname = 'outlier_treatment'
        try:
            df = self.df.copy()
            df_stat = pd.DataFrame(df[datacolumn].describe()).T
            Q1, Q3 = df_stat['25%'].values[0], df_stat['75%'].values[0]

            IQR = Q3 - Q1
            lower_range = Q1 - (1.5 * IQR)
            upper_range = Q3 + (1.5 * IQR)

            df[datacolumn] = np.where(df[datacolumn] > upper_range, input_value, df[datacolumn])
            df[datacolumn] = np.where(df[datacolumn] < lower_range, input_value, df[datacolumn])

            return df, lower_range, upper_range
        except Exception as e:
            print(f"ERROR [{defname}] : {str(e)}")