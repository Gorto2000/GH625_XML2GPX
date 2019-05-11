#------------------------------------------------------------------------------
# GH625_XML2GPX
# (c) 2019 Christopher Thiele
#
# Python converter that transforms XML tracks from GlobalSat GH-625 sport
# watches to GPX tracks. The converter searches for all fitting XML files
# in a given folder (including all subfolders) and converts them one by one.
#
# Usage: "python gh625_xml2gpx [-w] path"
# By default, existing GPX files are not overwritten. The user can give
# the optional command line argument "-w" to overwrite existing GPX files.
#
# License: GPLv3
#------------------------------------------------------------------------------

from glob import glob
from sys import argv
from os import path
from SourceXMLDocument import SourceXMLDocument
from SourceXMLDocument import SourceFileError
from TargetXMLDocument import TargetXMLDocument

def areCommandLineArgumentsCorrect():
    # Either called like "gh625_xml2gpx -w path" or "gh625_xml2gpx path"
    if len(argv) != 2 and len(argv) != 3:
        print("Number of arguments not correct")
        return False

    if len(argv) == 3 and argv[1] != "-w":
        print("Arguments not correct: \"-w\" expected as first argument")
        return False

    return True


def getSearchExpressionFromCommandLineArguments():
    if len(argv) == 2:
        searchExpression = argv[1]
    elif len(argv) == 3:
        searchExpression = argv[2]
    else:
        return ""

    if pathExists(searchExpression) == False:
        print("Path " + searchExpression + " not found")
        return ""

    # If the user entered the path with backslashes, use normal slashes
    # instead. Python accepts slashes in windows, too.
    searchExpression = searchExpression.replace("\\", "/")
    if searchExpression.endswith("/") == False:
        searchExpression += "/"

    searchExpression += "**/*.xml"

    return searchExpression


def getOverwriteSwitchFromCommandLineArguments():
    if len(argv) == 3 and argv[1] == "-w":
        return True
    return False


def convertFile(filePath, overwriteSwitch):
    targetFilePath = getTargetFilePath(filePath)
    if fileExists(targetFilePath) == True and overwriteSwitch == False:
        print ("Conversion of " + filePath + " not possible: Target file exists")
        return

    try:
        sourceXMLDocument = SourceXMLDocument(filePath)
        print("Converting " + filePath + "...", end = " ")
    except SourceFileError as ex:
        print("Conversion of " + filePath + " not possible: " + ex.errorMessage)
        return

    sourceTrackPoints = sourceXMLDocument.getTrackPoints()

    targetXMLDocument = TargetXMLDocument(sourceXMLDocument.getFileTitle(), sourceXMLDocument.buildDateTimeString(sourceXMLDocument.getStartDateTime()))
    targetXMLDocument.addTrackPoints(sourceTrackPoints)
    targetXMLDocument.writeToFile(getTargetFilePath(filePath))
    print("Done")


def getTargetFilePath(sourceFilePath):
    return sourceFilePath.replace("xml", "gpx")


def fileExists(filePath):
    return path.isfile(filePath)


def pathExists(searchPath):
    return path.isdir(searchPath)


def main():
    if areCommandLineArgumentsCorrect() == True:
        searchExpression = getSearchExpressionFromCommandLineArguments()
        overwriteSwitch = getOverwriteSwitchFromCommandLineArguments()
        if searchExpression != "":
            filePaths = glob(searchExpression, recursive=True)
            for filePath in filePaths:
                convertFile(filePath.replace("\\", "/"), overwriteSwitch)


if __name__ == '__main__':
    main()
