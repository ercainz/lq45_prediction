from datetime import datetime

import sys
#sys.path.insert(0, '..')
#sys.path.insert(0, '..//src//models')
sys.path.insert(0, 'src/models')

import global_func as gf
import predict

config_dir = 'config\\'

def get_data_from_api():
    defname = 'main_predict|get_data_from_api'
    try: 
        input_list = [7071.4419,
                      546.128,
                      24.75,
                      451.64,
                      9.7775,
                      10.5467,
                      5.1009,
                      4.3317]

        #raise Exception('===== xxx =====')

        return input_list
    except Exception as e:
        print(f"ERROR [{defname}] : {str(e)}")
        return None
#==========================================================================================================================#
#==========================================================================================================================#
def parsing_data_to_dataframe(predictor, input_data):
    defname = 'main_predict|parsing_data_to_dataframe'
    try: 
        df = predictor.parsing_data(input_list=input_data)
        return df
    except Exception as e:
        print(f"ERROR [{defname}] : {str(e)}")
        return None
#==========================================================================================================================#
#==========================================================================================================================#
def load_predictor(save_to_pkl=False):
    defname = 'main_predict|load_predictor'
    try:     
        models_dir = gf.read_config(config_dir=config_dir, section='DIR', key='MODELS')
        data_remod_dir = gf.read_config(config_dir=config_dir, section='DIR', key='DATA_REMODEL')

        model_fname = models_dir + gf.read_config(config_dir=config_dir, section='FILENAME', key='MODEL') + '.pkl'
        model = gf.load_from_pkl(filename=model_fname)

        scaler_fname = data_remod_dir + gf.read_config(config_dir=config_dir, section='FILENAME', key='SCALER') + '.pkl'
        scaler = gf.load_from_pkl(filename=scaler_fname)

        Predictor = predict.Predictor(model=model, scaler=scaler)

        if save_to_pkl:
            predictor_fname = models_dir + gf.read_config(config_dir=config_dir, section='FILENAME', key='PREDICTOR') + datetime.now().strftime("_%Y%m%d_%H%M") + '.pkl'
            gf.save_as_pkl(obj=Predictor, filename=predictor_fname, compress=6)

        return Predictor
    except Exception as e:
        print(f"ERROR [{defname}] : {str(e)}")
#==========================================================================================================================#
#==========================================================================================================================#
def pipeline():
    defname = 'main_predict|pipeline'
    try:
        print('Predicting, please wait....')
        input_data = get_data_from_api()

        if input_data is None:
            raise Exception('Failed to get data from api')

        Predictor = load_predictor(save_to_pkl=False)
        df = parsing_data_to_dataframe(predictor=Predictor, input_data=input_data)

        print(df)

        return True
    except Exception as e:
        print(f"ERROR [{defname}] : {str(e)}")
    finally:
        print(f'Finished')
#==========================================================================================================================#
#==========================================================================================================================#

if __name__ == "__main__":
    pipeline()