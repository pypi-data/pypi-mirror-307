import matplotlib.pyplot as plt

def plot_pcoa_results(coords, title, filename):
    plt.figure(figsize=(8, 6))
    plt.scatter(coords[:, 0], coords[:, 1], c='blue', label='Samples')
    plt.xlabel('PC1')
    plt.ylabel('PC2')
    plt.title(title)
    plt.grid(True)
    plt.savefig(filename)
    plt.close()
