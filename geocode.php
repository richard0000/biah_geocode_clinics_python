<?php
/*
 * @author silvio.gamarra.ext@boehringer-ingelheim.com
 * @date 06/27/2018
 *
 * The purpose of this script file is to enhace the process of import clinics into the https://int-us038.bi-customerhub.com, 
 * due to after a change made for improve the precision in the lat & lng values for each clinic, changing form contact geocode 
 * for each zipcode, to calling the same service, but for each different address, the process went slower.
 *
 * PRO: The improvement is very significant, because the service only stores the csv values in the local database, and the 
 * values are complete in the csv.
 * CON: This solution is not definitive, knowing that the user has to run it locally before uploading the file.
 *
 **/

/**
 * Country where the clinics are placed
 *
 */
$country = 'NL';

/**
 * Counter for rows to be writed
 *
 */
$row = 1;

/**
 * Name of the existing csv file to take as reference
 *
 */
$inputName = 'csvNLoptouts';

/**
 * Name of the new csv file to be created
 *
 */
$outputName = 'csvNLoptouts2';

/**
 * Open a new file (the one to be created)
 *
 */
$fileOutput = fopen($outputName . ".csv", "w");

/**
 * Header to be writed as first row in the new csv ($outputName)
 *
 */
$headerOutput = 
"clinicId|Type|Zip|Latitude|Longitude|Town|City|Street|State|County|Country|ClinicName|URL|OptOut|LastModified_by|address|phone|HG_FLAG|TR_FLAG|NG_FLAG|PRV_FLAG|FL_FLAG|MERIAL_VAX_FLAG|PUREVAX_FLAG";

/**
 * Write the first row to the new csv (headers)
 *
 */
fputcsv($fileOutput, explode('|', $headerOutput), "|");

/**
 * Open the existing csv file to spin trough
 *
 */
if (($file = fopen($inputName . ".csv", "r")) !== false) {
    $data = fgetcsv($file, 5000, "|");
    while (($data = fgetcsv($file, 5000, "|")) !== false) {
        $numero = count($data);
        $row++;

        $geoData = array(
            'id'      => $data[0],
            'address' => $data[15],
            'zip'     => $data[2],
        );

        $geoCoOrdinates = _get_geocode($geoData);

        $dataOutput =
            $data[0] . "|" . "veterinary clinic" . "|" .
            $data[2] . "|" .
            $geoCoOrdinates['lat'] . "|" .
            $geoCoOrdinates['lng'] . "|" . "|" .
            $data[6] . "|" . "|" .
            $data[8] . "|" . "|" . $country . "|" .
            $data[11] . "|" . "|" .
            $geoCoOrdinates['opt_out'] . "|" . "|" .
            $data[15] . "|" .
            $data[16] . "|" . "N" . "|" . "N" . "|" . "N" . "|" . "N" . "|" . "Y" . "|" . "N" . "|" . "N";

        $fields = array();
        fputcsv($fileOutput, explode('|', $dataOutput), "|");
    }

    fclose($file);
    fclose($fileOutput);
}

/**
 * Given a clinic data (country, zipcode and address), call geocode with different criteria to get the lat & long values
 * Criteria A: componets->country + zipcode & address -> address
 * Criteria B: componets->country & address -> address + zipcode
 * Criteria C: componets->country & address -> zipcode (In this last case, opt_out = 1, because of the imprecision)
 *
 */
function _get_geocode($geoData)
{
    $opt_out = 0;

    $service_data = _defineURL($geoData, 'A');

    if ($service_data == null) {
        $service_data = _defineURL($geoData, 'B');

        if ($service_data == null) {
            $service_data = _defineURL($geoData, 'C');
            $opt_out      = 1;
        }
    }

    $centerLat = isset($service_data[0]['geometry']['location']['lat']) ? $service_data[0]['geometry']['location']['lat'] : null;
    $centerLng = isset($service_data[0]['geometry']['location']['lng']) ? $service_data[0]['geometry']['location']['lng'] : null;

    $geoCoOrdinates['lat']     = $centerLat;
    $geoCoOrdinates['lng']     = $centerLng;
    $geoCoOrdinates['opt_out'] = $opt_out;

    return $geoCoOrdinates;
}

/**
 * Given a criteria, build the URL to contact GeoCode
 *
 */
function _defineURL($geoData, $criteria)
{
    $service_url               = 'https://maps.googleapis.com/maps/api/geocode/json';
    $service_key               = 'AIzaSyB6YAqeEFMu0ohvdr8h2Z6jhJW17pQSeII';
    $country = 'NL';


    switch ($criteria) {
        case 'A':
            $request_url = $service_url . '?components=country:' . $country . '|postal_code:' . str_replace(' ', '', $geoData['zip']) . '&address=' . str_replace(' ', '+', 
$geoData['address']) . '&key=' . $service_key;
            break;
        case 'B':
            $request_url = $service_url . '?components=country:' . $country . '&address=' . str_replace(' ', '+', $geoData['address']) . ',' .  str_replace(' ', '', $geoData['zip']) . 
'&key=' . $service_key;
            break;
        case 'C':
            $request_url = $service_url . '?components=country:' . $country . '&address=' . str_replace(' ', '', $geoData['zip']) . '&key=' . $service_key;
            break;
    }

    $service_response = null;
    $success          = _contatGeoCode($service_response, $request_url, $geoData, $criteria);

    if($success){
        echo "Clinic '" . $geoData['id'] . "' succeeded with criteria: " . $criteria . PHP_EOL;
    }

    return $success ? $service_response['results'] : null;
}

/**
 * Given a URL that haves a criteria to contact GoeCode, call to get lat & long values
 *
 */
function _contatGeoCode(&$service_response, $request_url, $geoData, $criteria)
{
    try {
        $ch = curl_init();
        curl_setopt($ch, CURLOPT_URL, $request_url);
        curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
        $service_response = json_decode(curl_exec($ch), true);
        curl_close($ch);
    } catch (Exception $e) {
        $service_response = null;
    }

    return determineSucces($service_response, $request_url, $geoData, $criteria);
}

/**
 * Given a response from geoCode, determine if it was successful or not
 *
 */
function determineSucces($service_response, $request_url, $geoData, $criteria)
{
    $success = null;
    if ($service_response) {
        $service_data = isset($service_response['results']) ? $service_response['results'] : null;
        if ($service_data) {
            $success = isset($service_response['results'][0]['geometry']) ? $service_response['results'][0]['geometry'] : null;
        }
    }

    return $success;
}
