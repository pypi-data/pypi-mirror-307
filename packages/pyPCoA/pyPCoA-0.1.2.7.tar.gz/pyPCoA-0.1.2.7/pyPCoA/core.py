import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import argparse

def load_data(file_path):
    """
    Load data from an Excel file and preprocess it, adjusting for samples as columns.

    Parameters:
        file_path (str): Path to the Excel file.

    Returns:
        pandas.DataFrame: Preprocessed data as a DataFrame.
    """
    data = pd.read_excel(file_path, header=0, index_col=0)  # OTU IDをインデックスとして読み込む
    data = data.T  # 転置してサンプルが行になるようにする
    data = data.apply(pd.to_numeric, errors='coerce').fillna(0)  # 数値に変換し、欠損値を0で置き換える
    # 各列（サンプル）の合計を1に正規化
    data = data.div(data.sum(axis=0), axis=1)
    return data

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

def pcoa(distance_matrix):
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
    df = pd.DataFrame(coords[:, :2], columns=['PC1', 'PC2'])
    df['Sample'] = sample_ids
    df.to_csv(filename, index=False, quoting=1)

def plot_pcoa_results(coords, title, filename):
    plt.figure(figsize=(8, 6))
    plt.scatter(coords[:, 0], coords[:, 1], c='blue', label='Samples')
    plt.xlabel('PC1')
    plt.ylabel('PC2')
    plt.title(title)
    plt.grid(True)
    plt.savefig(filename)
    plt.close()

def compute_and_save_pcoa(file_path, distance_type='jaccard', output_filename='PCoA_results.csv', plot_filename='PCoA_plot.png', plot=False):
    data = load_data(file_path)
    sample_ids = data.index  # サンプルIDを行名から取得

    # 距離行列の計算
    if distance_type == 'jaccard':
        distance_matrix = compute_ruzicka_distance_matrix(data)
    elif distance_type == 'braycurtis':
        distance_matrix = compute_bray_curtis_distance_matrix(data)
    else:
        raise ValueError("Invalid distance type. Choose 'jaccard' or 'braycurtis'.")

    # PCoAの実行
    coords = pcoa(distance_matrix)

    # Bray-CurtisのPC2を-1倍
    if distance_type == 'braycurtis':
        coords[:, 1] = -coords[:, 1]

    # PCoA結果の保存
    save_pcoa_results(coords, sample_ids, output_filename)

    # PCoA結果のプロット
    if plot:
        plot_title = f'PCoA Plot ({distance_type.capitalize()} Distance)'
        plot_pcoa_results(coords, plot_title, plot_filename)

def main():
    parser = argparse.ArgumentParser(description='Compute PCoA using Jaccard or Bray-Curtis distances.')
    parser.add_argument('--input', required=True, help='Path to the input Excel file.')
    parser.add_argument('--distance', choices=['jaccard', 'braycurtis'], default='jaccard', help='Type of distance to compute.')
    parser.add_argument('--output', default='PCoA_results.csv', help='Output CSV filename.')
    parser.add_argument('--plot', action='store_true', help='Enable plotting of PCoA results.')
    parser.add_argument('--plot_filename', default='PCoA_plot.png', help='Output plot image filename.')
    args = parser.parse_args()

    compute_and_save_pcoa(args.input, distance_type=args.distance, output_filename=args.output, plot_filename=args.plot_filename, plot=args.plot)

if __name__ == "__main__":
    main()
