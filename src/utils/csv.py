import csv


def read_csv_content_to_array(file_path, delimiter=","):
    data = []
    with open(file_path) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=delimiter)
        for row in csv_reader:
            data.append(row)
    return data
