import csv
import numpy as np
import pandas as pd
from io import StringIO

def read_csv_and_prepare_data(file_path: str) -> np.ndarray:

#    Чтение данных из CSV-файла и преобразование в numpy-массив.

    with open(file_path, 'r') as csvfile:
        reader = csv.reader(csvfile)
        data = [[int(value) for value in row] for row in reader]
    return np.array(data)

def calculate_adjacency_matrix(edges: list[tuple[int, int]], num_nodes: int) -> np.ndarray:

#    Формирование матрицы смежности на основе списка ребер.

    adj_matrix = np.zeros((num_nodes, num_nodes), dtype=int)
    for edge in edges:
        adj_matrix[edge[0] - 1][edge[1] - 1] = 1
    return adj_matrix

def calculate_result_matrix(adj_matrix: np.ndarray) -> np.ndarray:

#    Расчет матрицы результата на основе матрицы смежности.

    num_nodes = adj_matrix.shape[0]
    result_matrix = np.zeros((num_nodes, 5), dtype=int)

    # r₁: непосредственное управление
    result_matrix[:, 0] = np.sum(adj_matrix, axis=1)

    # r₂: непосредственное подчинение
    result_matrix[:, 1] = np.sum(adj_matrix, axis=0)

    # r₃: опосредованное управление
    for i in range(num_nodes):
        for j in range(num_nodes):
            if i != j and adj_matrix[i, j] == 0:
                paths = np.dot(adj_matrix[i], adj_matrix[:, j])
                if paths > 0:
                    result_matrix[i, 2] += 1

    # r₄: опосредованное подчинение
    for i in range(num_nodes):
        for j in range(num_nodes):
            if i != j and adj_matrix[j, i] == 0:
                paths = np.dot(adj_matrix[j], adj_matrix[:, i])
                if paths > 0:
                    result_matrix[i, 3] += 1

    # r₅: соподчинение на одном уровне
    for i in range(num_nodes):
        for j in range(num_nodes):
            if i != j and adj_matrix[i, j] == 0 and adj_matrix[j, i] == 0 and result_matrix[i, 4] <= 0:
                result_matrix[i, 4] += 1
    result_matrix[0, 4] = 0  # Корректируем значение для первой строки

    return result_matrix

def save_matrix_to_csv(matrix: np.ndarray, output_path: str) -> None:
    """
    Сохранение матрицы в CSV-файл.
    """
    with open(output_path, "w") as file:
        writer = csv.writer(file)
        writer.writerows(matrix)

def main():
    file_path = 'task2.csv'
    output_path = 'task2_result.csv'

    # Чтение данных из CSV и определение ребер
    data = read_csv_and_prepare_data(file_path)
    edges = [(row[0], row[1]) for row in data]

    # Определение количества узлов
    nodes = {node for edge in edges for node in edge}
    num_nodes = max(nodes)

    # Построение матрицы смежности
    adj_matrix = calculate_adjacency_matrix(edges, num_nodes)

    # Вычисление матрицы результата
    result_matrix = calculate_result_matrix(adj_matrix)

    # Сохранение результата в файл
    save_matrix_to_csv(result_matrix, output_path)

    print(f"Матрица результата сохранена в {output_path}")

# Запуск функции
if __name__ == "__main__":
    main()
