import numpy as np
import pandas as pd
from datetime import datetime

import sys
sys.path.insert(0, '..')
import global_func as gf

class Predictor():
    def __init__(self, model, scaler):
        self.model = model
        self.scaler = scaler
        self.input_dict = {'date':'yyyymmdd'
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
    def __input_validation(self, input_list):
        defname = 'Predictor|__input_validation'
        invalid_msg = ''
        result = False, invalid_msg
        try:
            # date:
            try:
                if len(input_list[0]) != 8:
                    raise Exception

                date = datetime.strptime(input_list[0], "%Y%m%d")
                result = True
            except:
                invalid_msg = "`date` format must be `yyyymmdd`"
                print(f"Validation failed : {invalid_msg}")
                return False, invalid_msg
            
            return result, invalid_msg
        except Exception as e:
            print(f"ERROR [{defname}] : {str(e)}")
            return False, invalid_msg
    #==========================================================================================================================#
    #==========================================================================================================================#
    def parsing_data(self, input_list):
        defname = 'Predictor|parsing_data'
        err_validation_msg = ''
        try:
            input_list_copy = input_list.copy()

            # convert to float
            for i in range(1,len(input_list_copy)):
                input_list_copy[i] = float(input_list_copy[i])
                if np.isnan(input_list_copy[i]):
                    input_list_copy[i] = float(0)

            is_valid, err_validation_msg = self.__input_validation(input_list=input_list_copy)
            if not is_valid:
                raise Exception('Failed to pass `Input-Validation` Test')         

            data = self.input_dict.copy()
            i=0
            for key in data:
                data[key] = [input_list_copy[i]]
                i += 1

            df_result = pd.DataFrame.from_dict(data)
            df_result.set_index('date', drop=True, inplace=True)
            df_result.index = pd.to_datetime(df_result.index)

            return df_result, err_validation_msg
        except Exception as e:
            print(f"ERROR [{defname}] : {str(e)}")
            return None, err_validation_msg
    #==========================================================================================================================#
    #==========================================================================================================================#
    def get_pred_value(self, dataframe):
        defname = 'Predictor|get_pred_value'
        try:
            forecast,_ = self.model.predict(n_periods=len(dataframe), 
                                            X=dataframe,
                                            return_conf_int=True)

            return forecast.values
        except Exception as e:
            print(f"ERROR [{defname}] : {str(e)}")
    #==========================================================================================================================#
    #==========================================================================================================================#        
    def forecast_evaluation(self, x_dataframe, y_data, name):
        defname = 'Predictor|forecast_evaluation'
        try:
            forecast,conf_int = self.model.predict(n_periods=len(y_data), 
                                                   X=x_dataframe,
                                                   return_conf_int=True)

            df_result = pd.concat([x_dataframe.reset_index(),
                                    pd.DataFrame(y_data, columns=['actual']),
                                    pd.DataFrame(forecast, columns=['pred']).reset_index(drop=True)],
                                    axis=1).set_index('date')
            df_result = df_result.loc[:, df_result.columns.isin(['actual','pred'])].copy()
            df_result.name = name
            return df_result
        except Exception as e:
            print(f"ERROR [{defname}] : {str(e)}")
    #==========================================================================================================================#
    #==========================================================================================================================#