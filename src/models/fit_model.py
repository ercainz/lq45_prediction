import pmdarima as pm

def modelling(train_dataframe):
    defname = 'fit_model|train_dataframe'
    try:
        exogenous = train_dataframe.loc[:, train_dataframe.columns[1:]]
        sarimax = pm.auto_arima(train_dataframe['lq45'], 
                                X=exogenous,
                                test='adf',
                                m=12, seasonal=True,
                                start_p=1, start_q=1,
                                max_p=3, max_q=3, 
                                start_P=0, 
                                d=None, D=1,
                                trace=True,
                                error_action='ignore',  
                                suppress_warnings=True, 
                                stepwise=True)
        return sarimax
    except Exception as e:
        print(f"ERROR [{defname}] : {str(e)}")
#==========================================================================================================================#
#==========================================================================================================================#