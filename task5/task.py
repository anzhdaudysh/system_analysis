import json
import numpy as np


def load_matrix_from_file(filepath: str):
    with open(filepath, 'r') as file:
        cluster_data = json.load(file)

    cluster_data = [group if isinstance(group, list) else [group] for group in cluster_data]
    total_elements = sum(len(group) for group in cluster_data)

    adjacency_matrix = [[1] * total_elements for _ in range(total_elements)]

    visited_elements = []
    for group in cluster_data:
        for visited in visited_elements:
            for current in group:
                adjacency_matrix[current - 1][visited - 1] = 0
        for current in group:
            visited_elements.append(int(current))

    return np.array(adjacency_matrix)


def identify_clusters(adjacency_matrix, mat1, mat2):
    conflicting_pairs = []

    for row in range(len(adjacency_matrix)):
        for col in range(row + 1, len(adjacency_matrix)):
            if adjacency_matrix[row][col] == 0 and adjacency_matrix[col][row] == 0:
                conflict = sorted([row + 1, col + 1])
                if conflict not in conflicting_pairs:
                    conflicting_pairs.append(conflict)

    results = [group[0] if len(group) == 1 else group for group in conflicting_pairs]
    return str(results)


def main(file1, file2):
    mat1 = load_matrix_from_file(file1)
    mat2 = load_matrix_from_file(file2)

    intersection_matrix = np.multiply(mat1, mat2)
    transposed_intersection = np.multiply(np.transpose(mat1), np.transpose(mat2))
    union_matrix = np.maximum(intersection_matrix, transposed_intersection)

    resulting_clusters = identify_clusters(union_matrix, mat1, mat2)
    return resulting_clusters


if __name__ == "__main__":
    print(main("example1.json", "example2.json"))
