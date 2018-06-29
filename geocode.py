# Author: Alexander Christoforides
# Date: June 28, 2018
#
# Description: This script is used to obtain the precise location data from
#              Google's Geocoding API. It is multithreadded so that it is capable
#              of running much faster than the sequential method. In case some
#              addresses can not be ran successfully. In order to find these,
#              the program will run the check_geocode_errors program to populate
#              a file with all of the errors.
#
# How To Run: python3 input.csv output.csv

import csv
import multiprocessing
import os
import requests
import sys

GOOGLE_MAPS_API_URL = 'https://maps.googleapis.com/maps/api/geocode/json'
API_KEY = ''

def geocode_worker(row):
    if row[3] == "" or row[4] == "":
        # Geocode and store in 2 variables

        full_address = row[15] # Address

        if row[6] != "": # City
            full_address += ", {}".format(row[6])
        if row[8] != "": # State
            full_address += ", {}".format(row[8])
        if row[10] != "": # Country
            full_address += ", {}".format(row[10])

        # Geocode the address
        request_url = GOOGLE_MAPS_API_URL + '?address={}&region={}&key={}'.format(full_address, row[10], API_KEY)
        req = requests.get(request_url)
        res = req.json()

        # We should only use the first result
        try:
            result = res['results'][0]
            lng = result['geometry']['location']['lng']
            lat = result['geometry']['location']['lat']

            # Add to list of things to write
            item_to_add = '{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}'.format(row[0], row[1], row[2], 
                                                                                                           lng, lat, row[5], row[6], 
                                                                                                           row[7], row[8], row[9], 
                                                                                                           row[10], row[11], row[12], 
                                                                                                           row[13], row[14], row[15], 
                                                                                                           row[16], row[17], row[18], 
                                                                                                           row[19], row[20], row[21], 
                                                                                                           row[22], row[23])
        except:
            lng = 'ERROR'
            lat = 'ERROR'
            # Add to list of things to write
            item_to_add = '{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}'.format(row[0], row[1], row[2], 
                                                                                                           lng, lat, row[5], row[6], 
                                                                                                           row[7], row[8], row[9], 
                                                                                                           row[10], row[11], row[12], 
                                                                                                           row[13], row[14], row[15], 
                                                                                                           row[16], row[17], row[18], 
                                                                                                           row[19], row[20], row[21], 
                                                                                                           row[22], row[23])

    else:
        # No need to geocode
        item_to_add = '{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}'.format(*row)
   
    print(item_to_add)
    return item_to_add

def get_old_rows():
    original_rows = []

    with open(sys.argv[2]) as csvfile:
        readCSV = csv.reader(csvfile, delimiter='|')
        for row in readCSV:
            original_rows.append(row)

    return original_rows

def main():
    if len(sys.argv) <= 3:
        print('[geocode.py][ERROR] Missing arguments. Should be in form "python geocode.py input.csv output.csv')
        sys.exit()

    API_KEY = sys.argv[1]

    print('[geocode.py] Storing old values locally...')
    original_rows = get_old_rows()

    print('[geocode.py] Running the workers...')
    pool = multiprocessing.Pool(processes=multiprocessing.cpu_count())
    new_rows = pool.map(geocode_worker, original_rows)

    print('[geocode.py] Writing output to file')
    output_file = open(sys.argv[3], 'w')
    with output_file:
        for row in new_rows:
            output_file.write(''.join(str(row)))
            output_file.write('\n')

    print('[geocode.py] Done!')
    print('[geocode.py] Running check_geocode_errors.py automatically...')

    os.system('python check_geocode_errors.py {}'.format(sys.argv[3]))

if __name__ == '__main__':
    main()