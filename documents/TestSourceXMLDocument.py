import unittest
from datetime import datetime, timezone
from documents.SourceXMLDocument import SourceXMLDocument

class TestSourceXMLDocument(unittest.TestCase):

    def test_buildDateTimeString(self):
        # Given
        dateTimeUTC = datetime(year=2019,
                               month=5,
                               day=13,
                               hour=20,
                               minute=10,
                               second=17,
                               tzinfo=timezone.utc)
        # When
        dateTimeString = SourceXMLDocument.buildDateTimeString(dateTimeUTC)

        # Then
        self.assertEqual(dateTimeString, "2019-05-13T20:10:17.000Z")

if __name__ == '__main__':
    unittest.main()
