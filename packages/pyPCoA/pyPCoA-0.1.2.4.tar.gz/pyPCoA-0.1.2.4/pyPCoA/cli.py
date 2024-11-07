import argparse
from .core import compute_and_save_pcoa

def main():
    parser = argparse.ArgumentParser(description='PCoA analysis with pyPCoA')
    parser.add_argument('file_path', type=str, help='Path to the input Excel file')
    parser.add_argument('--distance_type', type=str, default='jaccard', choices=['jaccard', 'braycurtis'],
                        help='Distance type to use for PCoA')
    parser.add_argument('--output_filename', type=str, default='PCoA_results.csv', help='Filename for PCoA results')
    parser.add_argument('--plot_filename', type=str, default='PCoA_plot.png', help='Filename for PCoA plot')

    args = parser.parse_args()
    compute_and_save_pcoa(args.file_path, args.distance_type, args.output_filename, args.plot_filename)

if __name__ == '__main__':
    main()
