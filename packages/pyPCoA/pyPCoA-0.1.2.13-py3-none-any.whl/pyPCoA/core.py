import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import argparse
import csv

def load_data(file_path):
    """
    Excelファイルからデータを読み込み、サンプルが行になるように前処理します。

    Parameters:
        file_path (str): Excelファイルのパス。

    Returns:
        pandas.DataFrame: 前処理されたデータフレーム。
    """
    data = pd.read_excel(file_path, header=0, index_col=0)  # OTU IDをインデックスとして読み込む
    data = data.T  # 転置してサンプルが行になるようにする
    data = data.apply(pd.to_numeric, errors='coerce').fillna(0)  # 数値に変換し、欠損値を0で置き換える
    # 各行（サンプル）の合計を1に正規化
    data = data.div(data.sum(axis=1), axis=0)
    return data

def ruzicka_distance(u, v):
    """
    2つのベクトル間のRuzicka距離を計算します。

    Parameters:
        u, v (pandas.Series): 入力ベクトル。

    Returns:
        float: Ruzicka距離。
    """
    numerator = np.minimum(u, v).sum()
    denominator = np.maximum(u, v).sum()
    return 1 - numerator / denominator if denominator != 0 else 0

def compute_ruzicka_distance_matrix(data):
    """
    データに対してRuzicka距離行列を計算します。

    Parameters:
        data (pandas.DataFrame): 入力データ。

    Returns:
        numpy.ndarray: Ruzicka距離行列。
    """
    n_samples = data.shape[0]
    distance_matrix = np.zeros((n_samples, n_samples))
    for i in range(n_samples):
        for j in range(i + 1, n_samples):
            dist = ruzicka_distance(data.iloc[i], data.iloc[j])
            distance_matrix[i, j] = dist
            distance_matrix[j, i] = dist
    return distance_matrix

def bray_curtis_distance(u, v):
    """
    2つのベクトル間のBray-Curtis距離を計算します。

    Parameters:
        u, v (pandas.Series): 入力ベクトル。

    Returns:
        float: Bray-Curtis距離。
    """
    numerator = np.abs(u - v).sum()
    denominator = (u + v).sum()
    return numerator / denominator if denominator != 0 else 0

def compute_bray_curtis_distance_matrix(data):
    """
    データに対してBray-Curtis距離行列を計算します。

    Parameters:
        data (pandas.DataFrame): 入力データ。

    Returns:
        numpy.ndarray: Bray-Curtis距離行列。
    """
    n_samples = data.shape[0]
    distance_matrix = np.zeros((n_samples, n_samples))
    for i in range(n_samples):
        for j in range(i + 1, n_samples):
            dist = bray_curtis_distance(data.iloc[i], data.iloc[j])
            distance_matrix[i, j] = dist
            distance_matrix[j, i] = dist
    return distance_matrix

def pcoa(distance_matrix):
    """
    主座標分析（PCoA）を実行します。

    Parameters:
        distance_matrix (numpy.ndarray): 距離行列。

    Returns:
        numpy.ndarray: PCoAの座標。
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
    PCoAの結果をCSVファイルに保存します。

    Parameters:
        coords (numpy.ndarray): PCoAの座標。
        sample_ids (list): サンプルIDのリスト。
        filename (str): 出力CSVファイル名。
    """
    df = pd.DataFrame(coords[:, :2], columns=['PC1', 'PC2'])
    df['Sample'] = sample_ids
    df.to_csv(filename, index=False, quoting=csv.QUOTE_ALL)

def plot_pcoa_results(coords, title, filename):
    """
    PCoAの結果をプロットし、画像ファイルとして保存します。

    Parameters:
        coords (numpy.ndarray): PCoAの座標。
        title (str): プロットのタイトル。
        filename (str): 出力画像ファイル名。
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
    入力データからPCoAの座標を計算し、結果を保存・プロットします。

    Parameters:
        file_path (str): 入力Excelファイルのパス。
        distance_type (str): 計算する距離の種類（'jaccard'または'braycurtis'）。
        output_filename (str): 出力CSVファイル名。
        plot_filename (str): 出力プロット画像ファイル名。
    """
    # データの読み込み
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
    elif distance_type == 'jaccard':    
        coords[:, 0] = -coords[:, 0]  
        coords[:, 1] = -coords[:, 1]  

    # PCoA結果の保存
    save_pcoa_results(coords, sample_ids, output_filename)

    # PCoA結果のプロット
    plot_title = f'PCoA Plot ({distance_type.capitalize()} Distance)'
    plot_pcoa_results(coords, plot_title, plot_filename)

def main():
    parser = argparse.ArgumentParser(description='JaccardまたはBray-Curtis距離を使用してPCoAを計算します。')
    parser.add_argument('--input', required=True, help='入力Excelファイルのパスを指定します。')
    parser.add_argument('--distance', choices=['jaccard', 'braycurtis'], default='jaccard', help='計算する距離の種類を指定します。')
    parser.add_argument('--output', default='PCoA_results.csv', help='出力CSVファイル名を指定します。')
    parser.add_argument('--plot', default='PCoA_plot.png', help='出力プロット画像ファイル名を指定します。')
    args = parser.parse_args()

    compute_and_save_pcoa(args.input, distance_type=args.distance, output_filename=args.output, plot_filename=args.plot)

if __name__ == "__main__":
    main()
