import pandas as pd
import numpy as np
import pickle

def create_pkl(obj, pkl):
    defname = 'global_func|create_pkl'
    try:
        with open(pkl, 'wb') as f:
            pickle.dump(obj, f)
            print(f'"{pkl}" ({type(obj)}) has been created')

    except Exception as e:
        print(f"ERROR [{defname}] : {str(e)}")
#==========================================================================================================================#
#==========================================================================================================================#
def load_pkl(pkl):
    defname = 'global_func|load_pkl'
    try:
        with open(pkl, 'rb') as f:
            return pickle.load(f)

    except Exception as e:
        print(f"ERROR [{defname}] : {str(e)}")
#==========================================================================================================================#
#==========================================================================================================================#