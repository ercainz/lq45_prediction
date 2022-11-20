from datetime import datetime

import sys
#sys.path.insert(0, '..')
#sys.path.insert(0, '..//src//models')
sys.path.insert(0, 'src/models')

import global_func as gf
import predict

config_dir = 'config\\'

def load_predictor():
    defname = 'main_predict|load_predictor'
    try:     
        models_dir = gf.read_config(config_dir=config_dir, section='DIR', key='MODELS')

        model = gf.load_from_pkl(filename=f'{models_dir}sarimax.pkl')
        scaler = gf.load_from_pkl(filename=f'{models_dir}scaler.pkl')
        Predictor = predict.Predictor(model=model, scaler=scaler)

        predictor_filename = f'{models_dir}predictor_{datetime.now().strftime("%Y%m%d_%H%M")}.pkl'
        gf.save_as_pkl(obj=Predictor, filename=predictor_filename, compress=6)

        return Predictor
    except Exception as e:
        print(f"ERROR [{defname}] : {str(e)}")
#==========================================================================================================================#
#==========================================================================================================================#
def pipeline():
    defname = 'main_predict|pipeline'
    try:
        print('Predicting, please wait....')
        Predictor = load_predictor()
        print(Predictor)

        return True
    except Exception as e:
        print(f"ERROR [{defname}] : {str(e)}")
    finally:
        print(f'Finished')
#==========================================================================================================================#
#==========================================================================================================================#

if __name__ == "__main__":
    pipeline()