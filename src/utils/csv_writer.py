import csv

def save_to_csv(filename, row):

    with open(filename, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(row)