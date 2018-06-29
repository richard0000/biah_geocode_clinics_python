import csv
import sys

data_to_write = []

if len(sys.argv) <= 1:
    print('[check_geocode_errors.py][ERROR] Missing command-line argument for input file.')

print('[check_geocode_errors.py] Reading file for errors... (may take some time)')

with open(sys.argv[1]) as csvfile:
    readCSV = csv.reader(csvfile, delimiter='|')
    for row in readCSV:
        if "ERROR" in row:
            data_to_write.append(row)
        elif "clinicId" in row:
            data_to_write.append(row)

print('[check_geocode_errors.py] Writing errors to errors.csv')

output_file = open('errors.csv', 'w')
with output_file:
    for row in data_to_write:
        output_file.write('|'.join(row))
        output_file.write('\n')

print('[check_geocode_errors.py] Done!')