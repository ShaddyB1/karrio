import unittest
from unittest.mock import patch, ANY
from .fixture import gateway
from tests import logger

import karrio
import karrio.lib as lib
import karrio.core.models as models


class TestSEKOLogisticsTracking(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.TrackingRequest = models.TrackingRequest(**TrackingPayload)

    def test_create_tracking_request(self):
        request = gateway.mapper.create_tracking_request(self.TrackingRequest)

        self.assertEqual(request.serialize(), TrackingRequest)

    def test_get_tracking(self):
        with patch("karrio.mappers.seko.proxy.lib.request") as mock:
            mock.return_value = "{}"
            karrio.Tracking.fetch(self.TrackingRequest).from_(gateway)

            self.assertEqual(
                mock.call_args[1]["url"],
                f"{gateway.settings.server_url}",
            )

    def test_parse_tracking_response(self):
        with patch("karrio.mappers.seko.proxy.lib.request") as mock:
            mock.return_value = TrackingResponse
            parsed_response = (
                karrio.Tracking.fetch(self.TrackingRequest).from_(gateway).parse()
            )

            self.assertListEqual(lib.to_dict(parsed_response), ParsedTrackingResponse)

    def test_parse_error_response(self):
        with patch("karrio.mappers.seko.proxy.lib.request") as mock:
            mock.return_value = ErrorResponse
            parsed_response = (
                karrio.Tracking.fetch(self.TrackingRequest).from_(gateway).parse()
            )

            self.assertListEqual(lib.to_dict(parsed_response), ParsedErrorResponse)


if __name__ == "__main__":
    unittest.main()


TrackingPayload = {
    "tracking_numbers": ["89108749065090"],
}

ParsedTrackingResponse = []

ParsedErrorResponse = []


TrackingRequest = ["6994008906", "6994008907"]

TrackingResponse = """[
  {
    "ConsignmentNo": "WFY9001843",
    "Status": "International transit to destination country ",
    "Picked": null,
    "Delivered": null,
    "Tracking": "http://track.omniparcel.com/1481576-WFY9001843",
    "Reference1": "S5828797:0",
    "Events": [
      {
        "EventDT": "2021-03-01T21:47:50.643",
        "Code": null,
        "OmniCode": "OP-1",
        "Description": "Tracking number allocated & order ready",
        "Location": "SAN BERNARDINO,CA,US",
        "Part": 1
      },
      {
        "EventDT": "2021-03-05T08:56:22.287",
        "Code": null,
        "OmniCode": "OP-3",
        "Description": "Processed through Export Hub",
        "Location": "Carson, CA,US",
        "Part": 1
      },
      {
        "EventDT": "2021-03-05T13:53:00.55",
        "Code": null,
        "OmniCode": "OP-4",
        "Description": "International transit to destination country ",
        "Location": "CARSON, CA,US",
        "Part": 1
      }
    ]
  }
]
"""

ErrorResponse = """{
  "Property": "Destination.Address.CountryCode",
  "Message": "CountryCode is required",
  "Key": "CountryCode",
  "Value": ""
}
"""
