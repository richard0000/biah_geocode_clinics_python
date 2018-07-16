# VetLocator Geocoder
## Description

This script is used to obtain the precise location data from Google's Geocoding 
API. It is multithreadded so that it is capable of running much faster than the 
sequential method. In case some addresses can not be ran successfully. 
In order to find these, the program will run the check_geocode_errors program to 
populate a file with all of the errors.

Note: The program expects the input file to have the same headings as the US
Clinic Data file standard. It will not work otherwise.

## Prerequisites

Any version of `requests`

## How to Use

Note: The program doesn't work on the bi-employees network. You have to run this
on bi-guest or on a network with less network restrictions.

Call Syntax for Geocode: `python geocode.py [API_Key] [input_file.csv] [output_file.csv]`

Note: When calling `geocode.py`, `check_geocode_errors.py` will be ran
automatically after `geocode.py` finishes.

Call Syntax for Check Geocode Errors: `python check_geocode_errors.py [file_to_check.csv]

## Author

Author: Alexander Christoforides

Email: alexander.christoforides@boehringer-ingelheim.com
