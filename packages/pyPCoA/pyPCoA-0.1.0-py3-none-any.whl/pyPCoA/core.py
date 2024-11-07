# core.py

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import argparse

def load_data(file_path):
    """
    Load data from an Excel file and preprocess it.

    Parameters:
        file_path (str): Path to the Excel file.

    Returns:
        pandas.DataFrame: Preprocessed data as a DataFrame.
    """
    data = pd.read_excel(file_path, header=0)
    return data

def ruzicka_distance(u, v):
    """
    Calculate Ruzicka distance between two vectors.

    Parameters:
        u, v (numpy.ndarray): Input vectors.

    Returns:
        float: Ruzicka distance.
    """
    numerator = np.minimum(u, v).sum()
    denominator = np.maximum(u, v).sum()
    return 1 - numerator / denominator if denominator != 0 else 0

def compute_ruzicka_distance_matrix(data):
    """
    Compute Ruzicka distance matrix for the given data.

    Parameters:
        data (numpy.ndarray): Input data.

    Returns:
        numpy.ndarray: Ruzicka distance matrix.
    """
    n_samples = data.shape[0]
    distance_matrix = np.zeros((n_samples, n_samples))
    for i in range(n_samples):
        for j in range(i + 1, n_samples):
            dist = ruzicka_distance(data[i], data[j])
            distance_matrix[i, j] = dist
            distance_matrix[j, i] = dist
    return distance_matrix

def bray_curtis_distance(u, v):
    """
    Calculate Bray-Curtis distance between two vectors.

    Parameters:
        u, v (numpy.ndarray): Input vectors.

    Returns:
        float: Bray-Curtis distance.
    """
    numerator = np.abs(u - v).sum()
    denominator = (u + v).sum()
    return numerator / denominator if denominator != 0 else 0

def compute_bray_curtis_distance_matrix(data):
    """
    Compute Bray-Curtis distance matrix for the given data.

    Parameters:
        data (numpy.ndarray): Input data.

    Returns:
        numpy.ndarray: Bray-Curtis distance matrix.
    """
    n_samples = data.shape[0]
    distance_matrix = np.zeros((n_samples, n_samples))
    for i in range(n_samples):
        for j in range(i + 1, n_samples):
            dist = bray_curtis_distance(data[i], data[j])
            distance_matrix[i, j] = dist
            distance_matrix[j, i] = dist
    return distance_matrix

def pcoa(distance_matrix):
    """
    Perform Principal Coordinates Analysis (PCoA).

    Parameters:
        distance_matrix (numpy.ndarray): Distance matrix.

    Returns:
        numpy.ndarray: PCoA coordinates.
    """
    n = distance_matrix.shape[0]
    H = np.eye(n) - np.ones((n, n)) / n
    B = -0.5 * H.dot(distance_matrix ** 2).dot(H)
    eigvals, eigvecs = np.linalg.eigh(B)
    idx = np.argsort(eigvals)[::-1]
    eigvals = eigvals[idx]
    eigvecs = eigvecs[:, idx]
    pos_idx = eigvals > 0
    eigvals = eigvals[pos_idx]
    eigvecs = eigvecs[:, pos_idx]
    coords = eigvecs * np.sqrt(eigvals)
    return coords

def save_pcoa_results(coords, sample_ids, filename):
    """
    Save PCoA results to a CSV file.

    Parameters:
        coords (numpy.ndarray): PCoA coordinates.
        sample_ids (list): List of sample IDs.
        filename (str): Output CSV filename.
    """
    df = pd.DataFrame(coords[:, :2], columns=['PC1', 'PC2'])
    df['Sample ID'] = sample_ids
    df.to_csv(filename, index=False)

def plot_pcoa_results(coords, title, filename):
    """
    Plot PCoA results and save the plot as an image file.

    Parameters:
        coords (numpy.ndarray): PCoA coordinates.
        title (str): Title of the plot.
        filename (str): Output image filename.
    """
    plt.figure(figsize=(8, 6))
    plt.scatter(coords[:, 0], coords[:, 1], c='blue', label='Samples')
    plt.xlabel('PC1')
    plt.ylabel('PC2')
    plt.title(title)
    plt.grid(True)
    plt.savefig(filename)
    plt.close()

def compute_and_save_pcoa(file_path, distance_type='jaccard', output_filename='PCoA_results.csv', plot_filename='PCoA_plot.png'):
    """
    Compute PCoA coordinates from input data, save the results, and plot the results.

    Parameters:
        file_path (str): Path to the input Excel file.
        distance_type (str): Type of distance to compute ('jaccard' or 'braycurtis').
        output_filename (str): Name of the output CSV file.
        plot_filename (str): Name of the output plot image file.
    """
    # データの読み込み
    data = load_data(file_path)
    sample_ids = data.iloc[:, 0].values
    data_values = data.iloc[:, 1:].apply(pd.to_numeric, errors='coerce').fillna(0).values

    # 距離行列の計算
    if distance_type == 'jaccard':
        distance_matrix = compute_ruzicka_distance_matrix(data_values)
    elif distance_type == 'braycurtis':
        distance_matrix = compute_bray_curtis_distance_matrix(data_values)
    else:
        raise ValueError("Invalid distance type. Choose 'jaccard' or 'braycurtis'.")

    # PCoAの実行
    coords = pcoa(distance_matrix)

    # JaccardのPC1を-1倍
    if distance_type == 'jaccard':
        coords[:, 0] = -coords[:, 0]

    # Bray-CurtisのPC1とPC2を-1倍
    if distance_type == 'braycurtis':
        coords[:, 0] = -coords[:, 0]
        coords[:, 1] = -coords[:, 1]

    # PCoA結果の保存
    save_pcoa_results(coords, sample_ids, output_filename)

    # PCoA結果のプロット
    plot_title = f'PCoA Plot ({distance_type.capitalize()} Distance)'
    plot_pcoa_results(coords, plot_title, plot_filename)

def main():
    parser = argparse.ArgumentParser(description='Compute PCoA using Jaccard or Bray-Curtis distances.')
    parser.add_argument('--input', required=True, help='Path to the input Excel file.')
    parser.add_argument('--distance', choices=['jaccard', 'braycurtis'], default='jaccard', help='Type of distance to compute.')
    parser.add_argument('--output', default='PCoA_results.csv', help='Output CSV filename.')
    args = parser.parse_args()

    compute_and_save_pcoa(args.input, distance_type=args.distance, output_filename=args.output)
if __name__ == "__main__":
    main()
