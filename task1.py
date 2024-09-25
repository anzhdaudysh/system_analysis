import sys
import csv

def get_csv_value(file_path, row_number, col_number):
    with open(file_path, newline='') as csvfile:
        reader = csv.reader(csvfile)
        for i, row in enumerate(reader):
            if i == row_number:
                return row[col_number]

if __name__ == "__main__":
    file_path = sys.argv[1]
    row_number = int(sys.argv[2])
    col_number = int(sys.argv[3])

    value = get_csv_value(file_path, row_number, col_number)
    print(value)

