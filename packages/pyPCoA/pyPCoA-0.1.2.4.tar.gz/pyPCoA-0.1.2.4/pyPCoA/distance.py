import numpy as np

def ruzicka_distance(u, v):
    numerator = np.minimum(u, v).sum()
    denominator = np.maximum(u, v).sum()
    return 1 - numerator / denominator if denominator != 0 else 0

def compute_ruzicka_distance_matrix(data):
    n_samples = data.shape[0]
    distance_matrix = np.zeros((n_samples, n_samples))
    for i in range(n_samples):
        for j in range(i + 1, n_samples):
            dist = ruzicka_distance(data.iloc[i], data.iloc[j])
            distance_matrix[i, j] = dist
            distance_matrix[j, i] = dist
    return distance_matrix

def bray_curtis_distance(u, v):
    numerator = np.abs(u - v).sum()
    denominator = (u + v).sum()
    return numerator / denominator if denominator != 0 else 0

def compute_bray_curtis_distance_matrix(data):
    n_samples = data.shape[0]
    distance_matrix = np.zeros((n_samples, n_samples))
    for i in range(n_samples):
        for j in range(i + 1, n_samples):
            dist = bray_curtis_distance(data.iloc[i], data.iloc[j])
            distance_matrix[i, j] = dist
            distance_matrix[j, i] = dist
    return distance_matrix
