import pickle
import numpy as np
from datetime import datetime
import pandas as pd



def save2pickle(data, path_name = 'data.pickle'):
  with open(path_name,'wb') as pickle_file:
    pickle.dump(data, pickle_file)

def read_pickle(path_name = 'data.pickle'):
  with open(path_name,'rb') as pickle_file:
    return pickle.load(pickle_file)

## Scale based on average of values (energy profiles)
def normalize_series_average(series_ori, m):
    '''average normalizaiton but return averge value of the window (for energy reading purpose). 
    Series should be positive (close to zero sum with net demand lead to issues)'''
    sliding = series_ori.shape[0]//m
    sample_series = series_ori.reshape(sliding, m)
    scaler_average = np.average(sample_series, axis=1)
    scaler_average = scaler_average.repeat(m)
    old_err_state = np.seterr(divide='ignore')
    normalized_arr = np.divide(series_ori, scaler_average)
    # handle zero division
    normalized_arr = np.nan_to_num(normalized_arr, nan=0)
    np.seterr(**old_err_state) 
    return normalized_arr, scaler_average

def scaler_recoverary_sum(series_normalised, scaler_average):
    return series_normalised*scaler_average

## Scale based on max and min values
def scaler_normalization(series_ori, m):
  '''amplitude 10 normalizaiton'''
  sliding = series_ori.shape[0]//m
  sample_series = series_ori.reshape(sliding, m)
  scaler_max = np.max(sample_series, axis=1)
  scaler_min = np.min(sample_series, axis=1)
  scaler_10 = (scaler_max - scaler_min)/10
  scaler_10 = scaler_10.repeat(m)
  series_normalised = series_ori/scaler_10
  return series_normalised, scaler_10

def scaler_recoverary(series_normalised, scaler_10):
  return series_normalised*scaler_10

## Scale based on daily average and derivative (weather data)
def scaler_normalization(series_ori, m):
  '''waiting to be finished'''
  sliding = series_ori.shape[0]//m
  sample_series = series_ori.reshape(sliding, m)
  scaler_max = np.max(sample_series, axis=1)
  scaler_min = np.min(sample_series, axis=1)
  scaler_10 = (scaler_max - scaler_min)/10
  scaler_10 = scaler_10.repeat(m)
  series_normalised = series_ori/scaler_10
  return series_normalised, scaler_10

def scaler_recoverary(series_normalised, scaler_10):
  return series_normalised*scaler_10



## Generate ideal profile

def ideal_profile_generator(daily_consumption, additional_generation, tariff, *constraints):
    '''
    input the daily consumption, the shape to follow, tariff profile, regulation_profile and constraints as profile
    all input profiles should be in the same shape.
    Constraints should be a list of two profiles, the first one is the lower bound and the second one is the upper bound.
    output is the ideal profile considering the constraints, consumption, and other inputs
    regulation service can be considered as contraints or additional generation
    priority: constraints > additional_generation > tariff 
    '''
    if len(constraints) == 2:
        min_bound = constraints[0]
        max_bound = constraints[1]
    elif len(constraints) == 1:
        min_bound = constraints[0]
        max_bound = np.full((additional_generation.shape), np.inf)
    else:
        print('No constraints are given')
        min_bound = np.zeros((additional_generation.shape))
        max_bound = np.full((additional_generation.shape), np.inf)

    ideal_profile_naive = np.maximum(additional_generation, min_bound)
    residual = daily_consumption - np.sum(ideal_profile_naive)

    if residual <= 0:
        return ideal_profile_naive * daily_consumption / ideal_profile_naive.sum()

    else:
        # Group timestamps by tariff
        unique_tariffs, inverse_indices = np.unique(tariff, return_inverse=True)
        for tariff_level in unique_tariffs:
            indices_at_this_tariff = np.where(tariff == tariff_level)[0]
            remaining_slots = len(indices_at_this_tariff)

            # Evenly distribute the residual energy across timestamps with the same tariff
            for i in indices_at_this_tariff:
                adjust = max_bound[i] - ideal_profile_naive[i]
                share_of_residual = residual / remaining_slots

                if share_of_residual >= adjust:
                    ideal_profile_naive[i] += adjust
                    residual -= adjust
                else:
                    ideal_profile_naive[i] += share_of_residual
                    residual -= share_of_residual
                
                remaining_slots -= 1

            if residual <= 0:
                break

    return ideal_profile_naive


def ramping_swinging_door(time_series, capacity, window_size, up_thres = 0.05, down_thres = 0.03):
    '''ramping and swinging door algorithm to detect the ramping event and swinging event'''
    up_amp = capacity*up_thres
    down_amp = capacity*down_thres
    window_size = int(window_size)
    sliding_steps = int(len(time_series)-window_size)
    ### initialise state
    up_labels = np.zeros((len(time_series)))
    down_labels = np.zeros((len(time_series)))
    for i in range(sliding_steps):
        for j in range(i,i+window_size):
            if time_series[j]-time_series[i]>up_amp:
                up_labels[i:j+1]=1
                break
            if time_series[i]-time_series[j]>down_amp:
                down_labels[i:j+1]=1
                break
    return up_labels, down_labels