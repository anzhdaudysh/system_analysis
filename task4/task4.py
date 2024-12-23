import numpy as np
import pandas as pd


def calculate_entropy(values):

    entropy = -np.sum(values * np.log2(values, where=(values > 0)))
    return entropy

def load_csv_data(filepath):

    df = pd.read_csv(filepath, index_col=0)
    return df.values


def main():
    data = load_csv_data('example.csv')
    total_count = data.sum()


    probabilities_A = data.sum(axis=1) / total_count
    probabilities_B = data.sum(axis=0) / total_count
    joint_probabilities = data / total_count

    joint_entropy = calculate_entropy(joint_probabilities)

    entropy_A = calculate_entropy(probabilities_A)

    entropy_B = calculate_entropy(probabilities_B)

    conditional_entropy = joint_entropy - entropy_A
    mutual_information = entropy_B - conditional_entropy

    results = [round(value, 2) for value in [joint_entropy, entropy_A, entropy_B, conditional_entropy, mutual_information]]
    return results


if __name__ == "__main__":
    print(main())
