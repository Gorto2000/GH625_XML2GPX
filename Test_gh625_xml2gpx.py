import unittest
from gh625_xml2gpx import *

class Test_gh625_xml2gpx(unittest.TestCase):

    def test_getTargetFilePath_Windows(self):
        # Given
        filePath = "C:\TestData\XYZ\1236454.xml"

        # When
        convertedFilePath = getTargetFilePath(filePath)

        # Then
        self.assertEqual(convertedFilePath, "C:\TestData\XYZ\1236454.gpx")

    def test_getTargetFilePath_Linux(self):
        # Given
        filePath = "/home/user_x/TestData/1236454.xml"

        # When
        convertedFilePath = getTargetFilePath(filePath)

        # Then
        self.assertEqual(convertedFilePath, "/home/user_x/TestData/1236454.gpx")

    def test_getTargetFilePath_Empty(self):
        # Given
        filePath = ""

        # When
        convertedFilePath = getTargetFilePath(filePath)

        # Then
        self.assertEqual(convertedFilePath, "")

if __name__ == '__main__':
    unittest.main()
