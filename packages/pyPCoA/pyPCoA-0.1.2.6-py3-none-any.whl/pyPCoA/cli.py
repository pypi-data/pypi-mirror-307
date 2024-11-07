### cli.py
import argparse
from .core import compute_and_save_pcoa

def main():
    parser = argparse.ArgumentParser(description='Perform PCoA analysis and save the results.')
    parser.add_argument('file_path', type=str, help='Path to the input data file')
    parser.add_argument('--distance_type', type=str, choices=['jaccard', 'braycurtis'], default='jaccard', help='Type of distance metric to use')
    parser.add_argument('--output_filename', type=str, default='PCoA_results.csv', help='Filename for saving the PCoA results')
    parser.add_argument('--plot_filename', type=str, default='PCoA_plot.png', help='Filename for saving the PCoA plot')
    
    args = parser.parse_args()
    
    # PCoAの計算と結果保存
    compute_and_save_pcoa(
        file_path=args.file_path,
        distance_type=args.distance_type,
        output_filename=args.output_filename,
        plot_filename=args.plot_filename
    )

if __name__ == "__main__":
    main()
