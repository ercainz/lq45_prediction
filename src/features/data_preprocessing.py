import pandas as pd
import numpy as np
from statsmodels.tsa.seasonal import seasonal_decompose

import sys
sys.path.insert(0, '..')
import global_func as gf

class DataPreprocessing():
    def __init__(self):
        pass
    #==========================================================================================================================#
    #==========================================================================================================================#
    def resampling(self, dataframe, interval='M', resampling_method='mean', fillna_method='ffill'):
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

        resampling_method :
            mean,
            median
        '''
        defname = 'DataPreprocessing|resampling'
        try:
            if resampling_method.lower() == 'mean':
                df = dataframe.resample(interval).mean().fillna(method=fillna_method).copy()
            elif resampling_method.lower() == 'median':
                df = dataframe.resample(interval).median().fillna(method=fillna_method).copy()
            else:
                raise Exception(f'resampling_method must be mean or median')
            return df
        except Exception as e:
            print(f"ERROR [{defname}] : {str(e)}")
    #==========================================================================================================================#
    #==========================================================================================================================#
    def enriching(self, dataframe):
        defname = 'DataPreprocessing|enriching'
        try:
            df = dataframe.copy()
            df['dom_total'] = df['dom_b'] + df['dom_s']
            df['dom_net'] = df['dom_b'] - df['dom_s']
            df['for_total'] = df['for_b'] + df['for_s']
            df['for_net'] = df['for_b'] - df['for_s']

            return df
        except Exception as e:
            print(f"ERROR [{defname}] : {str(e)}")
    #==========================================================================================================================#
    #==========================================================================================================================#
    def set_target(self, dataframe, datacolumn='lq45', future_days=4):
        defname = 'DataPreprocessing|set_target'
        try:
            df = dataframe.copy()
            df['target'] = df[datacolumn].shift(-1*future_days)
            return df
        except Exception as e:
            print(f"ERROR [{defname}] : {str(e)}")
    #==========================================================================================================================#
    #==========================================================================================================================#
    def splitting(self, dataframe, train_end, valid_end):
        defname = 'DataPreprocessing|splitting'
        try:
            df_train = dataframe.loc[dataframe.index <= pd.to_datetime(train_end),:].copy()            
            df_valid = dataframe.loc[np.logical_and(dataframe.index > pd.to_datetime(train_end),
                                                    dataframe.index <= pd.to_datetime(valid_end)),:].copy()
            df_test = dataframe.loc[dataframe.index > pd.to_datetime(valid_end),:].copy()

            return df_train, df_valid, df_test
        except Exception as e:
            print(f"ERROR [{defname}] : {str(e)}")
    #==========================================================================================================================#
    #==========================================================================================================================#
    def outlier_treatment(self, dataframe, datacolumn, input_value):
        defname = 'DataPreprocessing|outlier_treatment'
        try:
            df = dataframe.copy()
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
    #==========================================================================================================================#
    #==========================================================================================================================#
    def monthly_seasonal_feature(self, dataframe_train):
        defname = 'DataPreprocessing|monthly_seasonal_feature'
        try:
            df_train_monthly = self.resampling(dataframe=dataframe_train['lq45'],
                                                interval='M',
                                                resampling_method='median',
                                                fillna_method='ffill')

            seasonal_dec = seasonal_decompose(df_train_monthly,
                                              model='multiplicative', 
                                              period=12,
                                              extrapolate_trend='freq'
                                              )

            df = seasonal_dec.seasonal[:12].to_frame().reset_index()
            df['month'] = pd.DatetimeIndex(df.date).month
            df = df.drop(columns='date').set_index('month').sort_values('month').copy()

            return seasonal_dec, df
        except Exception as e:
            print(f"ERROR [{defname}] : {str(e)}")
    #==========================================================================================================================#
    #==========================================================================================================================#
    def enriching_seasonal(self, dataframe, df_seasonal):
        defname = 'DataPreprocessing|enriching_seasonal'
        try:
            df = dataframe.copy()
            if 'seasonal' in list(df.columns):
                raise Exception(f"Column 'seasonal' is already exists.\nTry using another dataframe.")

            df = df.reset_index().set_index(pd.DatetimeIndex(df.index).month, drop=True).join(df_seasonal).copy()
            df = df.sort_values('date').set_index('date', drop=True).copy()

            return df
        except Exception as e:
            print(f"ERROR [{defname}] : {str(e)}")
            return df
    #==========================================================================================================================#
    #==========================================================================================================================#