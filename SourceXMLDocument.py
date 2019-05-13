from xml.dom import minidom
from xml.parsers.expat import ExpatError
from datetime import timedelta, datetime, timezone
from copy import deepcopy
from re import split

class SourceFileError(Exception):
    errorMessage = ""
    def __init__(self, errorMessage):
        self.errorMessage = errorMessage

# A source file looks like this:
# <GH-625_Dataform>
#   <trackHeader>
#     <TrackID>517202011</TrackID>
#     <TrackName>2011-5-1</TrackName>
#     <StartTime>10:55:20</StartTime>
#     <During>06:14:52</During>
#     <TotalDist>33908</TotalDist>
#     <Calories>543</Calories>
#     ...
#   </trackHeader>
#   <trackLapMaster>
#   ...
#   </trackLapMaster>
#   <trackLapPoints>
#     <Sl_x0020_No>1</Sl_x0020_No>
#     <Latitude>49.298392</Latitude>
#     <Longitude>8.818915</Longitude>
#     <Altitude>138</Altitude>
#     <Speed>0.43</Speed>
#     <Heart_x0020_Rate>0</Heart_x0020_Rate>
#     <Interval_x0020_Time>0</Interval_x0020_Time>
#     <Index>517202011</Index>
#   </trackLapPoints>
#   <trackLapPoints>
#     <Sl_x0020_No>2</Sl_x0020_No>
#   ...
# </GH-625_Dataform>

class SourceXMLDocument(object):

    def __init__(self, filePath):
        self.readXMLFile(filePath)


    def readXMLFile(self, filePath):
        # First, read the file itself
        try:
            self.xmlFile = minidom.parse(filePath)
        except ExpatError:
            raise SourceFileError("XML not valid")

        # Is it a GH-625 XML file?
        rootElements = self.xmlFile.getElementsByTagName("GH-625_Dataform")
        if len(rootElements) != 1:
            raise SourceFileError("Wrong XML file content, must contain element 'GH-625_Dataform'")

        # If yes: Then parse the XML document
        self.readStartDateTime()
        self.readTrackPoints()
        self.convertFilePath2FileName(filePath)


    def convertFilePath2FileName(self, filePath):
        # C:\Tracks\2019\19473959.xml -> 19473959
        filePathParts = split("\W+", filePath)
        if len(filePathParts) > 2:
            self.fileName = filePathParts[len(filePathParts) - 2]
        else:
            self.fileName = ""


    def readStartDateTime(self):
        # Find local time zone
        localTimeZone = datetime.now(timezone.utc).astimezone().tzinfo

        # Get the date and the start time out of the XML document
        trackHeader = self.xmlFile.getElementsByTagName("trackHeader")[0]
        trackDate = trackHeader.getElementsByTagName("TrackName")[0].firstChild.nodeValue
        trackStartTime = trackHeader.getElementsByTagName("StartTime")[0].firstChild.nodeValue

        trackDateComponents = trackDate.split("-")
        if len(trackDateComponents) != 3:
            raise SourceFileError("Wrong date format in track header")
        trackStartTimeComponents = trackStartTime.split(":")
        if len(trackStartTimeComponents) != 3:
            raise SourceFileError("Wrong time format in track header")

        # Finally, create the datetime object and convert it to UTC
        self.startDateTime = datetime(year=int(trackDateComponents[0]),
                                      month=int(trackDateComponents[1]),
                                      day=int(trackDateComponents[2]),
                                      hour=int(trackStartTimeComponents[0]),
                                      minute=int(trackStartTimeComponents[1]),
                                      second=int(trackStartTimeComponents[2]),
                                      tzinfo=localTimeZone)
        self.fileTitle = self.startDateTime.strftime("%Y-%m-%d %H:%M:%S")
        self.startDateTime = self.startDateTime.astimezone(timezone.utc)


    def readTrackPoints(self):
        self.trackPoints = []
        trackPoints = self.xmlFile.getElementsByTagName("trackLapPoints")

        trackPointDateTime = deepcopy(self.getStartDateTime())

        for trackPoint in trackPoints:
            latitude = trackPoint.getElementsByTagName("Latitude")[0].firstChild.nodeValue
            longitude = trackPoint.getElementsByTagName("Longitude")[0].firstChild.nodeValue
            altitude = trackPoint.getElementsByTagName("Altitude")[0].firstChild.nodeValue
            duration = float(trackPoint.getElementsByTagName("Interval_x0020_Time")[0].firstChild.nodeValue.replace(",", "."))

            durationTimeDelta = timedelta(seconds=duration)
            trackPointDateTime += durationTimeDelta

            convertedTrackPoint = (latitude, longitude, altitude, duration, self.buildDateTimeString(trackPointDateTime))
            self.trackPoints.append(convertedTrackPoint)


    @staticmethod
    def buildDateTimeString(dateTime):
        dateTimeString = dateTime.isoformat()
        if dateTimeString[19] == "+":
            return dateTimeString[:19] + ".000Z"
        else:
            return dateTimeString[:23] + "Z"


    def getStartDateTime(self):
        return self.startDateTime


    def getTrackPoints(self):
        return self.trackPoints


    def getFileName(self):
        return self.fileName


    def getFileTitle(self):
        return self.fileTitle
