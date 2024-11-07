import pandas as pd

def load_data(file_path):
    data = pd.read_excel(file_path, header=0, index_col=0)  # OTU IDをインデックスとして読み込む
    data = data.T  # 転置してサンプルが行になるようにする
    data = data.apply(pd.to_numeric, errors='coerce').fillna(0)  # 数値に変換し、欠損値を0で置き換える
    # 各列（サンプル）の合計を1に正規化
    data = data.div(data.sum(axis=0), axis=1)
    return data

def save_pcoa_results(coords, sample_ids, filename):
    df = pd.DataFrame(coords[:, :2], columns=['PC1', 'PC2'])
    df['Sample'] = sample_ids
    df.to_csv(filename, index=False, quoting=1)
