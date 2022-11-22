import pandas as pd

def load_csv(csv_name):
    defname = 'load_data|load_csv'
    try:
        df = pd.read_csv(csv_name, parse_dates=['date'])
        df.set_index(['date'],inplace=True)
        return df
    except Exception as e:
        print(f"ERROR [{defname}] : {str(e)}")
#==========================================================================================================================#
#==========================================================================================================================#