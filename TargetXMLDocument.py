from xml.dom import minidom

class TargetXMLDocument(object):

    def __init__(self, fileTitle, startDateTime):
        self.createInitialTargetXMLDocument(fileTitle, startDateTime)


    def createInitialTargetXMLDocument(self, fileTitle, startDateTime):
        initialXMLString = ("<gpx version=\"1.1\" xmlns=\"http://www.topografix.com/GPX/1/1\" xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\""
                            " xsi:schemaLocation=\"http://www.topografix.com/GPX/1/1 http://www.topografix.com/GPX/1/1/gpx.xsd\""
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


    def addTrackPoints(self, trackPoints):
        for trackPoint in trackPoints:
            trackPointElement = self.targetXMLDocument.createElement("trkpt")
            trackPointElement.setAttribute("lat", trackPoint[0])
            trackPointElement.setAttribute("lon", trackPoint[1])

            elevationElement = self.targetXMLDocument.createElement("ele")
            elevationTextNode = self.targetXMLDocument.createTextNode(trackPoint[2])
            elevationElement.appendChild(elevationTextNode)
            trackPointElement.appendChild(elevationElement)

            timeElement = self.targetXMLDocument.createElement("time")
            timeTextNode = self.targetXMLDocument.createTextNode(trackPoint[4])
            timeElement.appendChild(timeTextNode)
            trackPointElement.appendChild(timeElement)

            self.trackSegment.appendChild(trackPointElement)
