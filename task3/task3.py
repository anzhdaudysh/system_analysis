import numpy as np
import pandas as pd
import math

matrix = pd.read_csv("task2_result.csv", header=None).values

entropy = 0
num_elements = len(matrix)

for i in range(num_elements):
    for j in range(num_elements):
        if matrix[i][j] != 0:
            probability = matrix[i][j] / (num_elements - 1)
            entropy += probability * math.log2(probability)


entropy = -entropy

print(entropy)
