import numpy as np
import pandas as pd 

import sys
sys.path.insert(0, '..')
import global_func as gf

class Predictor():
    def __init__(self, model, scaler):
        self.model = model
        self.scaler = scaler
    #==========================================================================================================================#
    #==========================================================================================================================#
    def forecasting(self, dataframe, name):
        def forecasting_raw(dataframe, sarimax):
            defname = 'Predictor|forecasting_raw'
            try:
                #sarimax = gf.load_pkl(pkl=r'..\models\pkl\sarimax(0,0,0)(2,1,0)(12).pkl')
                forecast,conf_int = sarimax.predict(n_periods=len(dataframe), 
                                                    X=dataframe.loc[:, dataframe.columns[1:]],
                                                    return_conf_int=True)

                df_result = pd.concat([dataframe.reset_index(),
                                        pd.DataFrame(forecast, columns=['pred']).reset_index(drop=True)],
                                        axis=1).set_index('date')

                df_result['lq45'] = df_result['pred']
                df_result.drop(['pred'], axis=1, inplace=True)
                df_result.rename(columns={"lq45": "pred_lq45"}, inplace=True)
                return df_result
            except Exception as e:
                print(f"ERROR [{defname}] : {str(e)}")


        defname = 'Predictor|forecasting'
        try:
            pred_dataframe = forecasting_raw(dataframe=dataframe, sarimax=self.model)
            scaler = self.scaler

            if pred_dataframe is None:
                raise Exception('pkl model not found')
            
            #scaler = gf.load_pkl(pkl=r'..\models\pkl\scaler.pkl')
            
            df_result = pd.concat([pd.DataFrame(dataframe['lq45']), pd.DataFrame(pred_dataframe['pred_lq45'])], axis=1)

            pred_inverse = scaler.inverse_transform(pred_dataframe)
            act_inverse = scaler.inverse_transform(dataframe)

            df_result['lq45_inv'] = act_inverse[:,0]
            df_result['pred_lq45_inv'] = pred_inverse[:,0]
            df_result.name = f'df_{name}'

            return df_result
        except Exception as e:
            print(f"ERROR [{defname}] : {str(e)}")
    #==========================================================================================================================#
    #==========================================================================================================================#