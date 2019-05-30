from xml.dom import minidom

class TargetXMLDocument(object):

    def __init__(self, fileTitle, startDateTime):
        self.createInitialTargetXMLDocument(fileTitle, startDateTime)


    def createInitialTargetXMLDocument(self, fileTitle, startDateTime):
        initialXMLString = ("<gpx version=\"1.1\" xmlns=\"http://www.topografix.com/GPX/1/1\" xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\""
                            " xsi:schemaLocation=\"http://www.topografix.com/GPX/1/1 http://www.topografix.com/GPX/1/1/gpx.xsd http://www.garmin.com/xmlschemas/TrackPointExtension/v1 http://www.garmin.com/xmlschemas/TrackPointExtensionv1.xsd\""
                            " xmlns:gpxtpx=\"http://www.garmin.com/xmlschemas/TrackPointExtension/v1\""
                            " creator=\"GH625_XML2GPX by Christopher Thiele\">"
                            "<metadata>"
                            "<name>" + fileTitle + "</name>"
                            "<author>"
                            "<name>GH625_XML2GPX converter for GH-625 GPS watches</name>"
                            "</author>"
                            "<time>" + startDateTime + "</time>"
                            "</metadata>"
                            "<trk>"
                            "<name>" + fileTitle + "</name>"
                            "<src></src>"
                            "<trkseg></trkseg>"
                            "</trk>"
                            "</gpx>")
        self.targetXMLDocument = minidom.parseString(initialXMLString)
        self.trackSegment = self.targetXMLDocument.getElementsByTagName("trkseg")[0]


    def writeToFile(self, targetFilePath):
        targetFile = open(targetFilePath, "w")
        self.targetXMLDocument.writexml(targetFile)
        targetFile.close()


    # A GPX track point looks like this (including the Garmin specific extension for the heart rate):
    # <trkpt lat="37.7833760" lon="-122.4072760">
    #   <ele>11.5</ele>
    #   <time>2015-01-19T21:24:25Z</time>
    #   <extensions>
    #     <gpxtpx:TrackPointExtension>
    #       <gpxtpx:hr>121</gpxtpx:hr>
    #     </gpxtpx:TrackPointExtension>
    #   </extensions>
    # </trkpt>
    def addTrackPoints(self, trackPoints):
        for trackPoint in trackPoints:
            trackPointElement = self.targetXMLDocument.createElement("trkpt")
            trackPointElement.setAttribute("lat", trackPoint["latitude"])
            trackPointElement.setAttribute("lon", trackPoint["longitude"])

            elevationElement = self.targetXMLDocument.createElement("ele")
            elevationTextNode = self.targetXMLDocument.createTextNode(trackPoint["altitude"])
            elevationElement.appendChild(elevationTextNode)
            trackPointElement.appendChild(elevationElement)

            timeElement = self.targetXMLDocument.createElement("time")
            timeTextNode = self.targetXMLDocument.createTextNode(trackPoint["trackPointDateTime"])
            timeElement.appendChild(timeTextNode)
            trackPointElement.appendChild(timeElement)

            # Heart rate has to be put into the extension sub-element
            extensionElement = self.targetXMLDocument.createElement("extensions")
            gtpxExtensionElement = self.targetXMLDocument.createElementNS("http://www.garmin.com/xmlschemas/TrackPointExtension/v1", "gpxtpx:TrackPointExtension")
            heartRateElement = self.targetXMLDocument.createElementNS("http://www.garmin.com/xmlschemas/TrackPointExtension/v1", "gpxtpx:hr")
            heartRateTextNode = self.targetXMLDocument.createTextNode(trackPoint["heartrate"])
            heartRateElement.appendChild(heartRateTextNode)
            gtpxExtensionElement.appendChild(heartRateElement)
            extensionElement.appendChild(gtpxExtensionElement)
            trackPointElement.appendChild(extensionElement)

            self.trackSegment.appendChild(trackPointElement)
