## Usage

> *IMPORTANT:* You have to read carefully the variables inside the geocode.php file to make it work properly
> *REQUIREMENTS:* You have to get installed php 5.6^ Locally.

### Steps

1. Configuring the values
- Place the csv file without latitude & longitude values (or with invalid ones, you may know that that values are the ones that are going to be replaced in the new file) at the root of 
the project (The same directory of geocode.php file).
- The most important values in the geocode.php file to be filled are:
	- country
	- inputName
	- outputName
 	- Set the proper flags in the $dataOutput variable

2. In a command prompt, at the root, type `php geocode.php`

You will see in the console, clinic by clinic, the criteria in which that one was successful getting the latitude & longitude values from geocode.
