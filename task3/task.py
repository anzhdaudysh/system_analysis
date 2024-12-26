import csv
import math
import argparse


def load_csv_as_matrix(filepath):
    data = []
    with open(filepath, 'r') as file:
        csv_reader = csv.reader(file, delimiter=',')
        for line in csv_reader:
            data.append(list(map(int, line)))
    return data


def compute_entropy(data_matrix):
    total_entropy = 0.0

    for row in data_matrix:
        row_total = sum(row)
        if row_total == 0:
            continue
        for element in row:
            if element > 0:
                probability = element / row_total
                total_entropy += probability * math.log2(probability)

    return -total_entropy


def main():
    parser = argparse.ArgumentParser(description="Compute the entropy of a given CSV file.")
    parser.add_argument('filepath', help="Path to the CSV file containing data.")
    args = parser.parse_args()

    data_matrix = load_csv_as_matrix(args.filepath)
    entropy_value = compute_entropy(data_matrix)
    print(round(entropy_value, 1))


if __name__ == "__main__":
    main()
