import pandas as pd

import global_func as gf
import data_preprocessing as dp

config_dir = 'config\\'

def load_predictor():
    defname = 'pipeline_predicting|load_predictor'
    try:     
        models_dir = gf.read_config(config_dir=config_dir, section='DIR', key='MODELS')
        predictor_fname = models_dir + gf.read_config(config_dir=config_dir, section='FILENAME', key='PREDICTOR') + '.pkl'
        Predictor = gf.load_from_pkl(filename=predictor_fname)

        return Predictor
    except Exception as e:
        print(f"ERROR [{defname}] : {str(e)}")
        return None
#==========================================================================================================================#
#==========================================================================================================================#
def parsing_data_to_dataframe(predictor, input_data):
    defname = 'pipeline_predicting|parsing_data_to_dataframe'
    try: 
        df, err_msg = predictor.parsing_data(input_list=input_data)
        return df, err_msg
    except Exception as e:
        print(f"ERROR [{defname}] : {str(e)}")
        return None
#==========================================================================================================================#
#==========================================================================================================================#
def data_pre_processing(predictor, input_dataframe):
    defname = 'pipeline_predicting|data_pre_processing'
    try:
        remodel_dir = gf.read_config(config_dir=config_dir, section='DIR', key='DATA_REMODEL')

        df_1 = input_dataframe.copy()
        
        # enriching features
        fname = remodel_dir + gf.read_config(config_dir=config_dir, section='FILENAME', key='DF_SEASONAL') + '.pkl'
        df_seasonal = gf.load_from_pkl(fname)
        df_2 = dp.enriching(dataframe=df_1)
        df_2 = dp.enriching_seasonal(dataframe=df_2, df_seasonal=df_seasonal)

        # outlier treatment
        fname = remodel_dir + gf.read_config(config_dir=config_dir, section='FILENAME', key='DF_OUTLIER') + '.pkl'
        df_value_for_outlier = gf.load_from_pkl(fname)
        df_3 = dp.outlier_treatment_batch(dataframe=df_2, df_value_for_outlier=df_value_for_outlier)
        
        # X standardizing
        scaler = predictor.scaler
        df_4 = dp.std_scaler_transform(dataframe=df_3, scaler=scaler, dataframe_with_target=False)

        return df_4
    except Exception as e:
        print(f"ERROR [{defname}] : {str(e)}")
        return None
#==========================================================================================================================#
#==========================================================================================================================#
def get_pred_value(predictor, final_dataframe):
    defname = 'pipeline_predicting|get_pred_value'
    try:
        df = predictor.get_pred_value(dataframe=final_dataframe)
        result = round(df[0], 3)

        return result
    except Exception as e:
        print(f"ERROR [{defname}] : {str(e)}")
        return None
#==========================================================================================================================#
#==========================================================================================================================#
def generate_api_feedback(value, final_dataframe):
    defname = 'pipeline_predicting|generate_api_feedback'
    try:
        day_a = pd.to_datetime(final_dataframe.tail(1).index.values[0]).strftime("%d-%b-%Y")
        day_b = pd.to_datetime(final_dataframe.tail(1).index.values[0]).strftime("%Y%m%d")
        target_days = int(gf.read_config(config_dir=config_dir, section='FEATURES', key='TARGET_DAYS'))
        target_feat = gf.read_config(config_dir=config_dir, section='FEATURES', key='TARGET_COL').upper()
        
        msg = f'{target_days} Business Days after {day_a}, {target_feat} value would be {value}'

        result = [day_b, value, msg]
        return result
    except Exception as e:
        print(f"ERROR [{defname}] : {str(e)}")
        return None
#==========================================================================================================================#
#==========================================================================================================================#
def pipeline(data_from_api):
    defname = 'pipeline_predicting|pipeline'
    pred_value = 0
    pred_msg = ''
    api_return = ['', pred_value, pred_msg]
    try:
        print('Predicting, please wait....')

        # Step 1
        Predictor = load_predictor()
        if Predictor is None:
            pred_msg = '`Predictor` pkl not found'
            raise Exception(pred_msg)
        
        # Step 2
        df, err_msg = parsing_data_to_dataframe(predictor=Predictor, input_data=data_from_api)
        if df is None:
            pred_msg = f'Failed to pass `Input-Validation` Test ({err_msg})'
            raise Exception(pred_msg)
        
        # Step 3
        df = data_pre_processing(predictor=Predictor, input_dataframe=df)
        if df is None:
            pred_msg = 'Failed to pass `Data Pre-Processing` Process'
            raise Exception(pred_msg)
        
        # Step 4
        pred_value = get_pred_value(predictor=Predictor, final_dataframe=df)
        if pred_value is None:
            pred_msg = 'Failed to pass `Predicting` Process'
            raise Exception(pred_msg)

        # Step 5
        api_return = generate_api_feedback(value=pred_value, final_dataframe=df)
        if api_return is None:
            pred_msg = 'Failed to pass `API Return`'
            raise Exception(pred_msg)

        return api_return
    except Exception as e:
        print(f"ERROR [{defname}] : {str(e)}")
        return ['', 0, pred_msg]
#==========================================================================================================================#
#==========================================================================================================================#