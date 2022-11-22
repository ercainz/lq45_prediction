from datetime import datetime

import global_func as gf
import load_data
import data_preprocessing as dp
import model_fitting as mf

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
        df_result = dp.resampling(dataframe=df_input, interval='B', resampling_method='median', fillna_method='ffill')
        return df_result
    except Exception as e:
        print(f"ERROR [{defname}] : {str(e)}")
#==========================================================================================================================#
#==========================================================================================================================#
def set_target(df_input):
    defname = 'main_remodel|set_target'
    try:     
        df_result = dp.set_target(dataframe=df_input, 
                                  datacolumn=gf.read_config(config_dir=config_dir, section='FEATURES', key='TARGET_COL'), 
                                  future_days=int(gf.read_config(config_dir=config_dir, section='FEATURES', key='TARGET_DAYS')))
        return df_result
    except Exception as e:
        print(f"ERROR [{defname}] : {str(e)}")
#==========================================================================================================================#
#==========================================================================================================================#
def data_enriching(df_input):
    defname = 'main_remodel|data_enriching'
    try:     
        df_result = dp.enriching(dataframe=df_input)
        return df_result
    except Exception as e:
        print(f"ERROR [{defname}] : {str(e)}")
#==========================================================================================================================#
#==========================================================================================================================#
def data_splitting(df_input):
    defname = 'main_remodel|data_splitting'
    try:
        df_train, df_valid, df_test = dp.splitting(dataframe=df_input, 
                                                   train_end=gf.read_config(config_dir=config_dir, section='FEATURES', key='TRAIN_END'),
                                                   valid_end=gf.read_config(config_dir=config_dir, section='FEATURES', key='VALID_END'))
        return df_train, df_valid, df_test
    except Exception as e:
        print(f"ERROR [{defname}] : {str(e)}")
#==========================================================================================================================#
#==========================================================================================================================#
def data_enriching_add_seasonal(df_input_train, df_input_valid, df_input_test):
    defname = 'main_remodel|data_enriching_add_seasonal'
    try:     
        _, df_seasonal = dp.monthly_seasonal_feature(dataframe_train=df_input_train)

        fname = remodel_dir + gf.read_config(config_dir=config_dir, section='FILENAME', key='DF_SEASONAL') + '.pkl'
        gf.save_as_pkl(obj=df_seasonal, filename=fname,compress=3)

        df_train = dp.enriching_seasonal(dataframe=df_input_train, df_seasonal=df_seasonal)
        df_valid = dp.enriching_seasonal(dataframe=df_input_valid, df_seasonal=df_seasonal)
        df_test = dp.enriching_seasonal(dataframe=df_input_test, df_seasonal=df_seasonal)

        return df_train, df_valid, df_test
    except Exception as e:
        print(f"ERROR [{defname}] : {str(e)}")
#==========================================================================================================================#
#==========================================================================================================================#
def stationary_transform(df_input_train, df_input_valid, df_input_test):
    defname = 'main_remodel|stationary_transform'
    try:
        pkl = remodel_dir + gf.read_config(config_dir=config_dir, section='FILENAME', key='NONSTATIONARY_COL_LIST') + '.pkl'

        df_train = dp.stationary_transform(dataframe=df_input_train, non_stationary_cols_pkl=pkl)
        df_valid = dp.stationary_transform(dataframe=df_input_valid, non_stationary_cols_pkl=pkl)
        df_test = dp.stationary_transform(dataframe=df_input_test, non_stationary_cols_pkl=pkl)

        return df_train, df_valid, df_test
    except Exception as e:
        print(f"ERROR [{defname}] : {str(e)}")
#==========================================================================================================================#
#==========================================================================================================================#
def outlier_handling(df_input_train, df_input_valid, df_input_test):
    defname = 'main_remodel|outlier_handling'
    try:     
        df_value_for_outlier = dp.get_value_for_outlier(train_dataframe=df_input_train, lo_perc=10.0, hi_perc=90.0)

        fname = remodel_dir + gf.read_config(config_dir=config_dir, section='FILENAME', key='DF_OUTLIER') + '.pkl'
        gf.save_as_pkl(obj=df_value_for_outlier, filename=fname,compress=3)

        df_train = dp.outlier_treatment_batch(dataframe=df_input_train, df_value_for_outlier=df_value_for_outlier)
        df_valid = dp.outlier_treatment_batch(dataframe=df_input_valid, df_value_for_outlier=df_value_for_outlier)
        df_test = dp.outlier_treatment_batch(dataframe=df_input_test, df_value_for_outlier=df_value_for_outlier)

        return df_train, df_valid, df_test
    except Exception as e:
        print(f"ERROR [{defname}] : {str(e)}")
#==========================================================================================================================#
#==========================================================================================================================#
def data_standardizing(df_input_train, df_input_valid, df_input_test):
    defname = 'main_remodel|data_standardizing'
    try:     
        scaler = dp.std_scaler_fitting(train_dataframe=df_input_train)

        fname = remodel_dir + gf.read_config(config_dir=config_dir, section='FILENAME', key='SCALER') + '.pkl'
        gf.save_as_pkl(obj=scaler, filename=fname,compress=3)

        df_train = dp.std_scaler_transform(dataframe=df_input_train, scaler=scaler)
        df_valid = dp.std_scaler_transform(dataframe=df_input_valid, scaler=scaler)
        df_test = dp.std_scaler_transform(dataframe=df_input_test, scaler=scaler)

        return df_train, df_valid, df_test
    except Exception as e:
        print(f"ERROR [{defname}] : {str(e)}")
#==========================================================================================================================#
#==========================================================================================================================#
def progress_label(current, max=8):
    print(f'  ================= ({current}/{max}) ================= ')
    return True
#==========================================================================================================================#
#==========================================================================================================================#
def pipeline(pickling=False):
    defname = 'main_remodel|pipeline'
    model_filename = models_dir + gf.read_config(config_dir=config_dir, section='FILENAME', key='MODEL') + datetime.now().strftime("_%Y%m%d_%H%M") + '.pkl'
    try:
        print('Remodelling, please wait....')
        raw_file = gf.read_config(config_dir=config_dir, section='DIR', key='DATA_RAW') + gf.read_config(config_dir=config_dir, section='FILENAME', key='DATASET') + '.csv'
        df = read_data(csv_file=raw_file)
        
        progress_label(1)
        df = resampling_daily(df_input=df)

        df = set_target(df_input=df)
        df = data_enriching(df_input=df)

        progress_label(2)
        df_train, df_valid, df_test = data_splitting(df_input=df)
        progress_label(3)
        df_train, df_valid, df_test = data_enriching_add_seasonal(df_input_train=df_train, df_input_valid=df_valid, df_input_test=df_test)

        #df_train, df_valid, df_test = stationary_transform(df_input_train=df_train, df_input_valid=df_valid, df_input_test=df_test)
        progress_label(4)
        df_train, df_valid, df_test = outlier_handling(df_input_train=df_train, df_input_valid=df_valid, df_input_test=df_test)
        progress_label(5)
        df_train, df_valid, df_test = data_standardizing(df_input_train=df_train, df_input_valid=df_valid, df_input_test=df_test)

        progress_label(6)
        model = mf.modelling(train_dataframe=df_train)
        #model = gf.load_from_pkl(filename=models_dir + gf.read_config(config_dir=config_dir, section='FILENAME', key='MODEL') + '.pkl')

        if model is None:
            raise Exception('Failed to retrain model')

        progress_label(7)
        if pickling:
            gf.save_as_pkl(obj=model, filename=model_filename,compress=6)

        progress_label(8)
        print(f'Finished, model filename: "{model_filename}"')
        return True
    except Exception as e:
        print(f"ERROR [{defname}] : {str(e)}")
#==========================================================================================================================#
#==========================================================================================================================#

if __name__ == "__main__":
    pipeline(pickling=True)