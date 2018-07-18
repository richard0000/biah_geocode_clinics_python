# VetLocator Geocoder
## Description

This script is used to obtain the precise location data from Google's Geocoding 
API. It is multithreadded so that it is capable of running much faster than the 
sequential method. In some cases, addresses can not be ran successfully. 
In order to find these, the program will look for errors and populate the
errors.csv file with all of the entires that failed.

Note: The program expects the input file to have the same headings as the US
Clinic Data file standard. It will not work otherwise.

## Prerequisites

Any version of `requests`

## How to Use

Note: The program doesn't work on the bi-employees network. You have to run this
on bi-guest or on a network with less network restrictions.

Call Syntax for Geocode: `python geocode.py [API_Key] [input_file.csv] [output_file.csv]`

## Author

Author: Alexander Christoforides

Email: alexander.christoforides@boehringer-ingelheim.com
