import numpy as np
import pandas as pd
from datetime import datetime
from pandas.tseries.offsets import BDay

import sys
sys.path.insert(0, '..')
import global_func as gf

class Predictor():
    def __init__(self, model, scaler):
        self.model = model
        self.scaler = scaler
        self.input_dict = {'date':'yyyymmdd'
                            ,'lq45':0
                            ,'jci':0
                            ,'idx30':0
                            ,'eido':0
                            ,'spy':0
                            ,'dom_b':0
                            ,'dom_s':0
                            ,'for_b':0
                            ,'for_s':0
                            }
    #==========================================================================================================================#
    #==========================================================================================================================#
    def forecasting(self, dataframe, name):
        def forecasting_raw(dataframe, sarimax):
            defname = 'Predictor|forecasting_raw'
            try:
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
    def parsing_data(self, prior, current):
        defname = 'Predictor|parsing_data'
        try:
            #date_current = datetime.strptime('20221122', "%Y%m%d")
            date_current = datetime.today() - BDay(1)
            date_prior = date_current - BDay(1)

            current_copy = current.copy()
            current_copy.insert(0, date_current.strftime("%Y%m%d"))

            prior_copy = prior.copy()
            prior_copy.insert(0, date_prior.strftime("%Y%m%d"))

            data = self.input_dict.copy()
            i=0
            for key in data:
                data[key] = [prior_copy[i], current_copy[i]]
                i += 1

            df_result = pd.DataFrame.from_dict(data)
            df_result.set_index('date', drop=True, inplace=True)
            df_result.index = pd.to_datetime(df_result.index)

            return df_result
        except Exception as e:
            print(f"ERROR [{defname}] : {str(e)}")
    #==========================================================================================================================#
    #==========================================================================================================================#