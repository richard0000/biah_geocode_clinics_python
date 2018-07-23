# Author: Alexander Christoforides
# Date: June 28, 2018
#
# Last Updated: July 23, 2018
#
# Description: This script is used to obtain the precise location data from
#              Google's Geocoding API. It is multithreadded so that it is capable
#              of running much faster than the sequential method. In some cases,
#              addresses can not be ran successfully. In order to find these,
#              the program will check for errors and populate a file with all 
#              of the errors.
#
# How To Run: python geocode_regular.py API_KEY

import argparse
import csv
import codecs
import getpass
import multiprocessing
import os
import requests
import sys
import urllib.parse

if len(sys.argv) <= 1:
    print("[ERROR] Missing command-line arguments. Should be in form 'python geocode_regular.py API_KEY'")
    sys.exit()

username = ''
password = ''
key = sys.argv[1]
input_file_name = ''
output_file_name = ''
file_delimiter = ''
proxy = ''

GOOGLE_MAPS_API_URL = 'https://maps.googleapis.com/maps/api/geocode/json'

def GetInput():
    global username
    username = input("Username: ")
    global password
    password = getpass.getpass()
    password = urllib.parse.quote(password.encode("UTF-8"))
    global input_file_name
    input_file_name = input("Input File: ")
    global output_file_name
    output_file_name = input("Output File: ")
    global file_delimiter
    file_delimiter = input("Delimiter: ")

    global proxy
    proxy = 'http://{}:{}@nahpx03.am.boehringer.com:3128'.format(str(username), str(password))

    os.environ['https_proxy'] = proxy
    os.environ['HTTPS_PROXY'] = proxy

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
        request_url = GOOGLE_MAPS_API_URL + '?address={}&region={}&key={}'.format(full_address, row[10], key)
        req = requests.get(request_url)
        res = req.json()

        # We should only use the first result
        try:
            result = res['results'][0]
            lng = result['geometry']['location']['lng']
            lat = result['geometry']['location']['lat']

            # Add to list of things to write
            item_to_add = '{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}'.format(row[0], row[1], row[2], 
                                                                                                           lat, lng, row[5], row[6], 
                                                                                                           row[7], row[8], row[9], 
                                                                                                           row[10], row[11], row[12], 
                                                                                                           row[13], row[14], row[15], 
                                                                                                           row[16], row[17], row[18], 
                                                                                                           row[19], row[20], row[21], 
                                                                                                           row[22], row[23])
        except:
            try:
                request_url = GOOGLE_MAPS_API_URL + '?components=country:{}|postal_code:{}&address={}&key={}'.format(row[10], row[2], row[15], key)
                req = requests.get(request_url)
                res = req.json()

                result = res['results'][0]
                lng = result['geometry']['location']['lng']
                lat = result['geometry']['location']['lat']
                
                item_to_add = '{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}'.format(row[0], row[1], row[2], 
                                                                                                           lat, lng, row[5], row[6], 
                                                                                                           row[7], row[8], row[9], 
                                                                                                           row[10], row[11], row[12], 
                                                                                                           row[13], row[14], row[15], 
                                                                                                           row[16], row[17], row[18], 
                                                                                                           row[19], row[20], row[21], 
                                                                                                           row[22], row[23])
            except:
                try:
                    request_url = GOOGLE_MAPS_API_URL + '?components=country:{}&address={}&key={}'.format(row[10], row[15] + ',' + row[2], key)
                    req = requests.get(request_url)
                    res = req.json()
                    
                    result = res['results'][0]
                    lng = result['geometry']['location']['lng']
                    lat = result['geometry']['location']['lat']

                    item_to_add = '{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}'.format(row[0], row[1], row[2], 
                                                                                                               lat, lng, row[5], row[6], 
                                                                                                               row[7], row[8], row[9], 
                                                                                                               row[10], row[11], row[12], 
                                                                                                               row[13], row[14], row[15], 
                                                                                                               row[16], row[17], row[18], 
                                                                                                               row[19], row[20], row[21], 
                                                                                                               row[22], row[23])
                except:
                    try:
                        request_url = GOOGLE_MAPS_API_URL + '?components=country:{}&address={}&key={}'.format(row[10], row[2], key)
                        req = requests.get(request_url)
                        res = req.json()

                        result = res['results'][0]
                        lng = result['geometry']['location']['lng']
                        lat = result['geometry']['location']['lat']
                        
                        item_to_add = '{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}'.format(row[0], row[1], row[2], 
                                                                                                                   lat, lng, row[5], row[6], 
                                                                                                                   row[7], row[8], row[9], 
                                                                                                                   row[10], row[11], row[12], 
                                                                                                                   str(1), row[14], row[15], 
                                                                                                                   row[16], row[17], row[18], 
                                                                                                                   row[19], row[20], row[21], 
                                                                                                                   row[22], row[23])
                    except:
                        lng = 'ERROR'
                        lat = 'ERROR'
                        print(res)
                        # Add to list of things to write
                        item_to_add = '{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}'.format(row[0], row[1], row[2], 
                                                                                                                       lat, lng, row[5], row[6], 
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
    global input_file_name
    input_file_name = str(input_file_name)
    original_rows = []

    with open(input_file_name) as csvfile:
        readCSV = csv.reader(csvfile, delimiter=file_delimiter)
        for row in readCSV:
            original_rows.append(row)
    
    return original_rows

def main():
    global output_file_name
    output_file_name = str(output_file_name)
    GetInput()

    print('[geocode.py] Storing old values locally...')
    original_rows = get_old_rows()

    print('[geocode.py] Running the workers...')
    pool = multiprocessing.Pool(processes=multiprocessing.cpu_count())
    new_rows = pool.map(geocode_worker, original_rows)

    print('[geocode.py] Writing output to file')
    output_file = open(output_file_name, 'w')
    with output_file:
        for row in new_rows:
            output_file.write(''.join(str(row)))
            output_file.write('\n')

    output_file.close()

    print('[geocode.py] Done!')
    print('[geocode.py] Running error checker...')

    data_to_write = []

    print('[geocode.py] Reading file for errors... (may take some time)')

    with open(output_file_name) as csvfile:
        readCSV = csv.reader(csvfile, delimiter='|')
        for row in readCSV:
            if "ERROR" in row:
                data_to_write.append(row)
            elif "clinicId" in row:
                data_to_write.append(row)

    print('[geocode.py] Writing errors to errors.csv')

    output_file = open('errors.csv', 'w')
    with output_file:
        for row in data_to_write:
            output_file.write('|'.join(row))
            output_file.write('\n')

    output_file.close()

    print('[geocode.py] Done!')

if __name__ == '__main__':
    main()
