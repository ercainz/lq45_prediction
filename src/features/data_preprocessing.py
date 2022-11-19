import pandas as pd
import numpy as np
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.tsa.stattools import adfuller
from sklearn.preprocessing import StandardScaler

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
    #==========================================================================================================================#
    #==========================================================================================================================#
    def stationary_checker_with_adfuller(self, dataframe, show_detail):
        defname = 'DataPreprocessing|stationary_checker_with_adfuller'
        try:
            df = dataframe.copy()
            list_non_stationary_cols = []
            for col in df.columns:
                adf_test = adfuller(df.dropna()[col], autolag = 'AIC')
                detail = '\n'
                detail += f'COLUMN                        : {col}\n'
                detail += f'  1. ADF                      : {adf_test[0]}\n'
                detail += f'  2. P-Value                  : {adf_test[1]}\n'
                detail += f'  3. Num Of Lags              : {adf_test[2]}\n'
                detail += f'  4. Num Of Observations Used : {adf_test[3]}\n'
                detail += f'  5. Critical Values 1%       : {adf_test[4]["1%"]}\n'
                detail += f'  6. Critical Values 5%       : {adf_test[4]["5%"]}\n'
                detail += f'  7. Critical Values 10%      : {adf_test[4]["10%"]}\n'
                detail += f'RESULT                        : '

                if adf_test[1] <= 0.05:
                    detail += f'STATIONARY\n'
                else:
                    detail += f'NON-STATIONARY\n'
                    list_non_stationary_cols.append(col)

                if show_detail:
                    print(detail)

            return list_non_stationary_cols
        except Exception as e:
            print(f"ERROR [{defname}] : {str(e)}")
    #==========================================================================================================================#
    #==========================================================================================================================#
    def convert_lags_differencing(self, dataframe, col, lag=1):
        defname = 'DataPreprocessing|convert_lags_differencing'
        try:
            df = dataframe.copy()
            df[col] = df[col].pct_change(periods=lag)
            return df[col]
        except Exception as e:
            print(f"ERROR [{defname}] : {str(e)}")
            return df
    #==========================================================================================================================#
    #==========================================================================================================================#
    def stationary_transform(self, dataframe, non_stationary_cols_pkl):
        defname = 'DataPreprocessing|stationary_transform'
        try:
            df = dataframe.copy()

            #cols = self.stationary_checker_with_adfuller(dataframe=df_train, show_detail=True)
            #gf.create_pkl(obj=cols, pkl=r'..\models\pkl\list_non_stationary_cols.pkl')
            cols = gf.load_pkl(pkl=non_stationary_cols_pkl)

            if cols is None:
                raise Exception('pkl not found')

            for col in df.columns:
                if col in cols:
                    df[col] = self.convert_lags_differencing(dataframe=df, col=col, lag=1)

            return df.dropna()
        except Exception as e:
            print(f"ERROR [{defname}] : {str(e)}")
            return df.dropna()
    #==========================================================================================================================#
    #==========================================================================================================================#
    def get_value_for_outlier(self, train_dataframe, lo_perc=25.00, hi_perc=75.00):
        defname = 'DataPreprocessing|get_value_for_outlier'
        try:
            lohi_list = []
            for col in train_dataframe.columns:
                lo_value = np.percentile(train_dataframe[col], lo_perc)
                hi_value = np.percentile(train_dataframe[col], hi_perc)
                lohi_list.append([col, lo_value, hi_value])

            df_result = pd.DataFrame(lohi_list, columns=['col_name','lo_value','hi_value']).set_index('col_name')

            return df_result
        except Exception as e:
            print(f"ERROR [{defname}] : {str(e)}")
    #==========================================================================================================================#
    #==========================================================================================================================#
    def outlier_treatment(self, dataframe, datacolumn, input_lower_value, input_upper_value):
        defname = 'DataPreprocessing|outlier_treatment'
        try:
            df = dataframe.copy()
            df_stat = pd.DataFrame(df[datacolumn].describe()).T
            Q1, Q3 = df_stat['25%'].values[0], df_stat['75%'].values[0]

            IQR = Q3 - Q1
            lower_range = Q1 - (1.5 * IQR)
            upper_range = Q3 + (1.5 * IQR)

            df[datacolumn] = np.where(df[datacolumn] > upper_range, input_upper_value, df[datacolumn])
            df[datacolumn] = np.where(df[datacolumn] < lower_range, input_lower_value, df[datacolumn])

            return df[datacolumn]
        except Exception as e:
            print(f"ERROR [{defname}] : {str(e)}")
    #==========================================================================================================================#
    #==========================================================================================================================#
    def outlier_treatment_batch(self, dataframe, df_value_for_outlier):
        defname = 'DataPreprocessing|outlier_treatment_batch'
        try:
            series_list = []
            for col in dataframe.iloc[:,dataframe.columns != 'seasonal'].columns:
                i_lo = df_value_for_outlier.loc[df_value_for_outlier.index == col,:]['lo_value'].values[0]
                i_hi = df_value_for_outlier.loc[df_value_for_outlier.index == col,:]['hi_value'].values[0]

                series = self.outlier_treatment(dataframe=dataframe, datacolumn=col, input_lower_value=i_lo, input_upper_value=i_hi)
                series_list.append(series)

            series_list.append(dataframe.seasonal)
            df_result = pd.concat(series_list,axis=1)

            return df_result
        except Exception as e:
            print(f"ERROR [{defname}] : {str(e)}")
    #==========================================================================================================================#
    #==========================================================================================================================#
    def std_scaler_fitting(self, train_dataframe):
        defname = 'DataPreprocessing|std_scaler_fitting'
        try:
            std_scaler = StandardScaler()
            std_scaler.fit(train_dataframe)
            return std_scaler
        except Exception as e:
            print(f"ERROR [{defname}] : {str(e)}")
    #==========================================================================================================================#
    #==========================================================================================================================#
    def std_scaler_transform(self, dataframe, scaler):
        defname = 'DataPreprocessing|std_scaler_transform'
        try:
            result = scaler.transform(dataframe)
            result = pd.DataFrame(result, columns=scaler.feature_names_in_)
            result['date'] = pd.to_datetime(dataframe.index)
            result.set_index('date', drop=True, inplace=True)

            return result
        except Exception as e:
            print(f"ERROR [{defname}] : {str(e)}")
    #==========================================================================================================================#
    #==========================================================================================================================#