# 修正後
from . import distance
from .io import load_data, save_pcoa_results
from .visualization import plot_pcoa_results
import pandas as pd
import numpy as np

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

def compute_and_save_pcoa(file_path, distance_type='jaccard', output_filename='PCoA_results.csv', plot_filename='PCoA_plot.png'):
    data = load_data(file_path)
    sample_ids = data.index  # サンプルIDを行名から取得

    # 距離行列の計算
    if distance_type == 'jaccard':
        distance_matrix = distance.compute_ruzicka_distance_matrix(data)
    elif distance_type == 'braycurtis':
        distance_matrix = distance.compute_bray_curtis_distance_matrix(data)
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
    plot_title = f'PCoA Plot ({distance_type.capitalize()} Distance)'
    plot_pcoa_results(coords, plot_title, plot_filename)
