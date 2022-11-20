from datetime import datetime
import numpy as np
import pandas as pd

import sys
#sys.path.insert(0, '..')
#sys.path.insert(0, '..//src//data')
#sys.path.insert(0, '..//src//features')
#sys.path.insert(0, '..//src//models')
sys.path.insert(0, 'src/data')
sys.path.insert(0, 'src/features')
sys.path.insert(0, 'src/models')

import global_func as gf
import load_data
import data_preprocessing
import fit_model

DataPrep = data_preprocessing.DataPreprocessing()
config_dir = 'config\\'
remodel_dir = gf.read_config(config_dir=config_dir, section='DIR', key='DATA_REMODEL')
models_dir = gf.read_config(config_dir=config_dir, section='DIR', key='MODELS')

def read_data(csv_file):
    defname = 'main_remodel|read_data'
    try:    
        df_result = load_data.load_csv(csv_file)
        return df_result
    except Exception as e:
        print(f"ERROR [{defname}] : {str(e)}")
#==========================================================================================================================#
#==========================================================================================================================#
def resampling_daily(df_input):
    defname = 'main_remodel|resampling_daily'
    try:     
        df_result = DataPrep.resampling(dataframe=df_input, interval='B', resampling_method='median', fillna_method='ffill')
        return df_result
    except Exception as e:
        print(f"ERROR [{defname}] : {str(e)}")
#==========================================================================================================================#
#==========================================================================================================================#
def data_enriching(df_input):
    defname = 'main_remodel|data_enriching'
    try:     
        df_result = DataPrep.enriching(dataframe=df_input)
        return df_result
    except Exception as e:
        print(f"ERROR [{defname}] : {str(e)}")
#==========================================================================================================================#
#==========================================================================================================================#
def data_splitting(df_input):
    defname = 'main_remodel|data_splitting'
    try:     
        df_train, df_valid, df_test = DataPrep.splitting(dataframe=df_input, train_end='2020-12-31', valid_end='2021-07-31')
        return df_train, df_valid, df_test
    except Exception as e:
        print(f"ERROR [{defname}] : {str(e)}")
#==========================================================================================================================#
#==========================================================================================================================#
def data_enriching_add_seasonal(df_input_train, df_input_valid, df_input_test):
    defname = 'main_remodel|data_enriching_add_seasonal'
    try:     
        _, df_seasonal = DataPrep.monthly_seasonal_feature(dataframe_train=df_input_train)
        gf.save_as_pkl(obj=df_seasonal, filename=f'{remodel_dir}value_for_seasonal.pkl',compress=3)

        df_train = DataPrep.enriching_seasonal(dataframe=df_input_train, df_seasonal=df_seasonal)
        df_valid = DataPrep.enriching_seasonal(dataframe=df_input_valid, df_seasonal=df_seasonal)
        df_test = DataPrep.enriching_seasonal(dataframe=df_input_test, df_seasonal=df_seasonal)

        return df_train, df_valid, df_test
    except Exception as e:
        print(f"ERROR [{defname}] : {str(e)}")
#==========================================================================================================================#
#==========================================================================================================================#
def stationary_transform(df_input_train, df_input_valid, df_input_test):
    defname = 'main_remodel|stationary_transform'
    try:     
        pkl = f'{remodel_dir}list_non_stationary_cols.pkl'

        df_train = DataPrep.stationary_transform(dataframe=df_input_train, non_stationary_cols_pkl=pkl)
        df_valid = DataPrep.stationary_transform(dataframe=df_input_valid, non_stationary_cols_pkl=pkl)
        df_test = DataPrep.stationary_transform(dataframe=df_input_test, non_stationary_cols_pkl=pkl)

        return df_train, df_valid, df_test
    except Exception as e:
        print(f"ERROR [{defname}] : {str(e)}")
#==========================================================================================================================#
#==========================================================================================================================#
def outlier_handling(df_input_train, df_input_valid, df_input_test):
    defname = 'main_remodel|outlier_handling'
    try:     
        df_value_for_outlier = DataPrep.get_value_for_outlier(train_dataframe=df_input_train, lo_perc=10.0, hi_perc=90.0)
        gf.save_as_pkl(obj=df_value_for_outlier, filename=f'{remodel_dir}value_for_outlier.pkl',compress=3)

        df_train = DataPrep.outlier_treatment_batch(dataframe=df_input_train, df_value_for_outlier=df_value_for_outlier)
        df_valid = DataPrep.outlier_treatment_batch(dataframe=df_input_valid, df_value_for_outlier=df_value_for_outlier)
        df_test = DataPrep.outlier_treatment_batch(dataframe=df_input_test, df_value_for_outlier=df_value_for_outlier)

        return df_train, df_valid, df_test
    except Exception as e:
        print(f"ERROR [{defname}] : {str(e)}")
#==========================================================================================================================#
#==========================================================================================================================#
def data_standardizing(df_input_train, df_input_valid, df_input_test):
    defname = 'main_remodel|data_standardizing'
    try:     
        scaler = DataPrep.std_scaler_fitting(train_dataframe=df_input_train)
        gf.save_as_pkl(obj=scaler, filename=f'{models_dir}scaler.pkl',compress=3)

        df_train = DataPrep.std_scaler_transform(dataframe=df_input_train, scaler=scaler)
        df_valid = DataPrep.std_scaler_transform(dataframe=df_input_valid, scaler=scaler)
        df_test = DataPrep.std_scaler_transform(dataframe=df_input_test, scaler=scaler)

        return df_train, df_valid, df_test
    except Exception as e:
        print(f"ERROR [{defname}] : {str(e)}")
#==========================================================================================================================#
#==========================================================================================================================#
def pipeline(pickling=False):
    defname = 'main_remodel|pipeline'
    model_filename = f'{models_dir}sarimax_{datetime.now().strftime("%Y%m%d_%H%M")}.pkl'
    try:
        print('Remodelling, please wait....')
        raw_dir = gf.read_config(config_dir=config_dir, section='DIR', key='DATA_RAW')
        df = read_data(csv_file=f'{raw_dir}dataset_Q122.csv')
        print('  [1/10]...')
        df = resampling_daily(df_input=df)
        print('  [2/10]...')
        df = data_enriching(df_input=df)
        print('  [3/10]...')
        df_train, df_valid, df_test = data_splitting(df_input=df)
        print('  [4/10]...')
        df_train, df_valid, df_test = data_enriching_add_seasonal(df_input_train=df_train, df_input_valid=df_valid, df_input_test=df_test)
        print('  [5/10]...')
        df_train, df_valid, df_test = stationary_transform(df_input_train=df_train, df_input_valid=df_valid, df_input_test=df_test)
        print('  [6/10]...')
        df_train, df_valid, df_test = outlier_handling(df_input_train=df_train, df_input_valid=df_valid, df_input_test=df_test)
        print('  [7/10]...')
        df_train, df_valid, df_test = data_standardizing(df_input_train=df_train, df_input_valid=df_valid, df_input_test=df_test)
        print('  [8/10]...')

        model = fit_model.modelling(train_dataframe=df_train)
        #model = gf.load_from_pkl(filename=f'{models_dir}sarimax.pkl')
        print('  [9/10]...')

        if pickling:
            gf.save_as_pkl(obj=model, filename=model_filename,compress=6)

        print('  [10/10]...')
        return True
    except Exception as e:
        print(f"ERROR [{defname}] : {str(e)}")
    finally:
        print(f'Finished, model filename: "{model_filename}"')
#==========================================================================================================================#
#==========================================================================================================================#

if __name__ == "__main__":
    pipeline(pickling=True)