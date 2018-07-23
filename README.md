# VetLocator Geocoder
## Description

This script is used to obtain the precise location data from Google's Geocoding 
API. It is multithreadded so that it is capable of running much faster than the 
sequential method. In some cases, addresses can not be ran successfully. 
In order to find these, the program will look for errors and populate the
errors.csv file with all of the entires that failed.

Note: The program expects the input file to have the same headings as the US
Clinic Data file standard. It will not work otherwise.

There are two versions of the program; one for ASCII encoded files and one
for UTF-16 encoded files (has foreign letters). In order to retain the special
characters when converting to a CSV file from a XLSX file for files with foreign characters, 
you must do the following:

1) Open the file in Excel
2) Click File in the top-left corner
3) Click "Save As"
4) Type in a name for the file and in the drop down menu, select "Unicode Text .txt"
5) Save the file and exit Excel
6) Go to the file in your file explorer and rename the extension to .csv
7) If a warning pops up, click "Yes".
8) Open up file in a text editor (which isn't notepad :D)
9) Find all double quotes in the file and delete them
10) Save file

## Prerequisites

Any version of `requests`

## How to Use

Note: The program doesn't work on the bi-employees network. You have to run this
on bi-guest or on a network with less network restrictions.

Call Syntax for `geocode_regular`: `python geocode_regular.py API_Key`

Call Syntax for `geocode_unicode`: `python geocode_unicode.py API_Key`

Note: The delimiter that is specified is the delimiter currently used in the input file.

## Author

Author: Alexander Christoforides

Email: alexander.christoforides@boehringer-ingelheim.com
