import numpy as np
from scipy.optimize import linear_sum_assignment
from sklearn.metrics import DistanceMetric
import scipy


class Code_book:
    '''
    This class includes different methods and implementations of our proposed codebook methods with Similarity Profile
    '''
    def __init__(self, time_series, m, mode='euclidean'):
        self.time_series = time_series
        self.m = m
        self.pattern_stack = []
        self.mode = mode
        self.sliding = time_series.shape[0]//m
        self.filtered_demand = time_series
        self._preprocessed = False

    @staticmethod 
    def weighted_DTW(series_1, series_2, weight = []):
        #### Series_1 and Series_2 are time series list, weight is weighted matrix list with two dimention
        #### default weight can be np.ones(len(series_1))
        #### weight cannot be negative (can make it square but need to think)
        l1 = series_1.shape[0]
        l2 = series_2.shape[0]
        cum_sum = np.full((l1 + 1, l2 + 1), np.inf)
        cum_sum[0, 0] = 0.
        if not len(weight):
            weight = np.ones((l1, l2))
        for i in range(l1):
            for j in range(l2):
                diff = (series_1[i] - series_2[j])
                distance = diff*diff*weight[i][j]
                cum_sum[i + 1, j + 1] = distance
                cum_sum[i + 1, j + 1] += min(cum_sum[i, j + 1],
                                                cum_sum[i + 1, j],
                                                cum_sum[i, j])
        acc_cost_mat = cum_sum[1:, 1:]
        return np.sqrt(acc_cost_mat[-1][-1])

    @staticmethod 
    # @jit(nopython=True)
    def flex_distance(series_a, series_b, *weight_matrix):
        '''By default, the time seies series_a and sereis_b should be same size and in a numpy array format, 
            but they can be different with slight change of the function. Weight_matrix is a tuple containing the '''
        ### weight_matrix: the weight matrix for the distance calculation based on residual distribution (how to convert)
        sliding = series_a.shape[0]
        if weight_matrix:
            weight_amp_metrix = weight_matrix[0]
            weight_tem_metrix = weight_matrix[1]
        else:
            scale = max(series_a)-min(series_a) if max(series_a)-min(series_a) > 0 else 1
            weight_amp_metrix = np.ones((sliding,sliding))*sliding
            weight_tem_metrix = np.ones((sliding,sliding))*scale
        # build the merged matrix for FD
        amplitude_matrix = np.zeros((sliding, sliding))
        temporal_matrix = np.zeros((sliding, sliding))
        for i in range(sliding):
            for j in range(sliding):
                amplitude_matrix[i][j] = series_a[i]-series_b[j]
                temporal_matrix[i][j] = i-j
        merged_matrix = np.abs(amplitude_matrix)*weight_amp_metrix + np.abs(temporal_matrix)*weight_tem_metrix
        # build the distance
        row_ind, col_ind = linear_sum_assignment(merged_matrix)
        # return merged_matrix[row_ind, col_ind].mean(), row_ind, col_ind if you want to check the selected route represented by row and col
        return merged_matrix[row_ind, col_ind].mean()
  
    @staticmethod 
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
    
    @staticmethod
    def scaler_recoverary_average(series_normalised, scaler_average):
        return series_normalised*scaler_average

    def pre_processing(self):
        if self._preprocessed:
            print('data already been preprocessed')
            return
        else:
            self.normalized_arr, self.scaler_average = self.normalize_series_average(self.time_series, self.m)
            self._preprocessed = True

    def post_processing(self):
        if not self._preprocessed:
            print('data has not been preprocessed')
            return
        else:
            recovered_series = self.time_series_recover(self.labels)
            recovered_series = self.scaler_recoverary_average(recovered_series, self.scaler_average)
            self.recovered_series = recovered_series

    def get_distance(self, series_1, series_2):
        if self.mode == 'euclidean':
            dis = DistanceMetric.get_metric('euclidean')
            distance = dis.pairwise([series_1, series_2])[0][1]
        elif self.mode == 'DTW':
            weighted_matrix = np.ones((self.m, self.m))
            distance = self.weighted_DTW(series_1, series_2, weighted_matrix)
        elif self.mode == 'wasserstein':
            distance = scipy.stats.wasserstein_distance(series_1, series_2)
        elif self.mode == 'flexibilityD':
            distance = self.flex_distance(series_1, series_2, np.ones((self.m))*self.m, np.ones((self.m)))       
        return distance
  
    def get_distance_matrix(self):
        m=self.m
        days = self.time_series.shape[0]//m
        distance_matrix = np.full((days, days), np.inf)
        if not hasattr(self, 'normalized_arr'):
            print('processing un-normalised raw data')
            time_series = self.time_series
        else:
            time_series = self.normalized_arr
        for i in range(days):
            current_pattern = time_series[i*m:i*m+m]
            for j in range(days):
                distance = self.get_distance(current_pattern, time_series[j*m:j*m+m])
                distance_matrix[i][j] = distance

        # Compute the mean of all elements in the matrix
        mean_value = np.mean(distance_matrix)

        # Compute quantile values (e.g., 25th, 50th, and 75th percentiles) for all elements in the matrix
        quantiles = np.quantile(distance_matrix, [0.25, 0.50, 0.75])
        # print(f"Mean: {mean_value}, 25th Percentile: {quantiles[0]}, 50th Percentile: {quantiles[1]}, 75th Percentile: {quantiles[2]}")
        self.distance_matrix = distance_matrix
        return distance_matrix, quantiles
  
    def simple_decomposition(self, series_data):
        ''' threshold 0,0 means the automatic mode'''
        m=self.m
        sliding = series_data.shape[0]//m
        distance_matrix = self.get_distance_matrix(series_data)
        distance_profile = np.zeros((sliding))
        discord_profile = np.zeros((sliding))
        average_profile = np.zeros((sliding))
        filtered_series = np.array([])
        distance_stack = np.array([])
        labels = ['normal' for i in range(sliding)]
        for i in range(sliding):
                for j in range(sliding):
                    # distance_matrix is inefficient, might needs to be changed 
                    if i!=j:
                        distance = distance_matrix[i][j]
                        distance_stack = np.append(distance_stack, [distance], axis=0)
                average_profile[i] = np.average(distance_matrix[i,:])
        d_max = np.sort(distance_stack)[-1]
        # if thres_m == 0 and thres_d == 0:
        #       thres_m = np.median(distance_stack)
        #       thres_d = np.median(distance_stack)
        ## Split it into two parts by n
        pos = distance_stack.shape[0]//4
        thres_m = np.sort(distance_stack)[pos]
        print(thres_m)
        thres_d = np.sort(distance_stack)[-pos]
        print(thres_d)
        for k in range(sliding):  
                counter_m = 0
                counter_d = 0
                for l in range(sliding):
                    distance = distance_matrix[k][l]
                    if distance < thres_m:
                        counter_m+=1
                    if distance > thres_d:
                        counter_d+=1
                distance_profile[k] = counter_m - average_profile[k]/d_max if d_max else counter_m
                discord_profile[k] = counter_d + average_profile[k]/d_max if d_max else counter_m
        RM = np.argsort(distance_profile)[-1]
        DS = np.argsort(discord_profile)[-1]
        for i in range(sliding):
            distance_m = distance_matrix[RM][i]
            distance_d = distance_matrix[DS][i]
            if distance_m<thres_m:
                labels[i] = 'repeated patterns'
            elif distance_d<=thres_m:
                labels[i] = 'abnormals'
            else:
                filtered_series = np.append(filtered_series, series_data[i*m:i*m+m], axis=0)
        labels[RM] = 'RM'
        labels[DS] = 'Discord'
        return distance_matrix, labels, filtered_series

    def desolve_time_series(self):
        m = self.m
        days = self.filtered_demand.shape[0]//m
        sample_Demand = self.filtered_demand
        counter = 0
        if days>4:
            test_matrix, labels, self.filtered_demand = self.simple_decomposition(sample_Demand)
            self.pattern_stack, normal_labels = self.desolve_time_series()
        #       print(normal_labels)
            for i in range(days):
                if labels[i] == 'RM':
                    RM_name = 'RM-'+str(len(self.pattern_stack))
                    labels[i] = RM_name
                    RM_pattern = sample_Demand[i*m:i*m+m]
                    self.pattern_stack.append(RM_pattern)
                if labels[i] == 'Discord':
                    Discord_name = 'Discord-'+str(len(self.pattern_stack))
                    labels[i] = Discord_name
                    Discord_pattern = sample_Demand[i*m:i*m+m]
                self.pattern_stack.append(Discord_pattern)
            for i in range(days):
                if labels[i] == 'repeated patterns':
                    labels[i] = RM_name
        #           sample_Demand[i*24:i*24+24] = RM_pattern
                if labels[i] == 'abnormals':
                    labels[i] = Discord_name
        #           sample_Demand[i*24:i*24+24] = Discord_pattern
                if labels[i] == 'normal':
                    labels[i] = normal_labels[counter]
                    counter+=1
            return self.pattern_stack, labels
        else:
            [self.pattern_stack.append(sample_Demand[i*m:i*m+m]) for i in range(days)]        
            return self.pattern_stack, ['reminders-'+str(i) for i in range(days)]

    def desolve_time_series_thre(self, threshold):
        '''Do not need to rebuild the distance matrix if it is already built'''
        m = self.m
        days = self.time_series.shape[0]//m
        labels = []
        if not hasattr(self, 'normalized_arr'):
            print('processing un-normalised raw data')
            time_series = self.time_series
        else:
            time_series = self.normalized_arr
        for i in range(days):
            current_pattern = time_series[i*m:i*m+m]
            distance_stack = []
            if self.pattern_stack:
                for j in self.pattern_stack:
                    distance = self.get_distance(j, current_pattern)
                    distance_stack.append(distance)
                if min(distance_stack)<threshold:
                    labels.append('patterns-'+str(distance_stack.index(min(distance_stack))))
                else:
                    self.pattern_stack.append(current_pattern)
                    labels.append('patterns-'+str(len(self.pattern_stack)-1))
                    # print('pattern stack distance is :', min(distance_stack))
            else:
                self.pattern_stack.append(current_pattern)
                labels.append('patterns-'+str(len(self.pattern_stack)-1))
        self.labels = labels
        return self.pattern_stack, labels

    def time_series_recover(self, labels):
        time_series = []
        indexs = [int(i.split('-')[1]) for i in labels]
        for i in indexs:
            time_series.extend(self.pattern_stack[i])
        return np.array(time_series)


