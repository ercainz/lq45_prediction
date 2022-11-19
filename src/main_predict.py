import sys
#sys.path.insert(0, '..')
#sys.path.insert(0, '..//src//models')
sys.path.insert(0, 'src/models')

import global_func as gf
import predict

def pipeline():
    defname = 'main_predict|pipeline'
    try:
        #sarimax = gf.load_pkl(pkl=r'models\pkl\sarimax(0,0,0)(2,1,0)(12).pkl')
        #scaler = gf.load_pkl(pkl=r'models\pkl\scaler.pkl')
        #Predictor = predict.Predictor(model=sarimax, scaler=scaler)
        Predictor = gf.load_pkl(pkl=r'models\pkl\predictor.pkl')

        print(Predictor)


        return True
    except Exception as e:
        print(f"ERROR [{defname}] : {str(e)}")
#==========================================================================================================================#
#==========================================================================================================================#

if __name__ == "__main__":
    pipeline()