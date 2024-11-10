"""
Pith / Cambium estimation
"""
__license__ = "GPL"
__author__ = "Sylvain Meignier"
__copyright__ = "Copyright 2023 Sylvain Meignier, Le Mans Université, LIUM (https://lium.univ-lemans.fr/)"

import numpy as np
import pandas as pd

def cambium_estimation(param, cambium, bark, sapwood, values):  
    if pd.isna(cambium) or pd.isna(bark): # no cambium or bark
        return pd.NA, pd.NA, pd.NA
    if cambium or bark: # cambium or bark persent
        return pd.NA, pd.NA, pd.NA
    elif pd.isna(sapwood) or ((sapwood > 0) and (sapwood >= len(values))) : # no sapwood
        return pd.NA, pd.NA, pd.NA
    elif param.cambium_estimation_method == 'log-log':
        return cambium_estimation_log_log(cambium, bark, sapwood, values)
    elif param.cambium_estimation_method == 'Lambert':
        return cambium_estimation_lambert(param.lambert_parameters, cambium, bark, sapwood, values)
    else:
        return pd.NA, pd.NA, pd.NA

def cambium_estimation_log_log(cambium, bark, sapwood, values):    
    nb = len(values)
    i = max(0, sapwood - 9)
    j = min(sapwood + 1, nb)
    rw10 = np.nanmean(values[i:j]) / 100
    x = 2.8102081 - 0.5331451 * np.log(rw10)
    estimation = int(np.round(np.exp(x))) + sapwood
    upper_bound = int(np.round(np.exp(x + 0.6087837))) + sapwood
    lower_bound = int(np.round(np.exp(x - 0.6087837))) + sapwood
    #print(f'sapwood={spawood}, estimation={estimation}, upper_bound={upper_bound}, lower_bound={lower_bound}')
    return lower_bound , estimation, upper_bound

def cambium_estimation_lambert(estimator, cambium, bark, sapwood, values):    
    lower_bound = estimator[0] + sapwood
    estimation = (estimator[0] + estimator[1]) // 2 + sapwood
    upper_bound = estimator[1] + sapwood
    return lower_bound , estimation, upper_bound

