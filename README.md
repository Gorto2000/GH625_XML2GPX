# GH625_XML2GPX
Python converter that transforms XML tracks from GH-625 watches to GPX tracks

## Usage
`python gh625_xml2gpx.py [-w] path`
* By default, existing GPX files are not overwritten. The user can add the
optional command line argument `-w` to overwrite existing GPX files.
* The given `path` is the starting point of the search for XML files.
XML files found in any subfolder are checked for the right content and
converted if possible. The GPX output file is placed into the same subfolder
than the original XML file.
* GPX hasn't defined an element for the heart rate. Thus, this converter
uses the Garmin extension for GPX trackpoints to store the heart rate numbers
form the original file.

## Unit Tests
* `python Test_gh625_xml2gpx.py`
* `python TestSourceXMLDocument.py`
