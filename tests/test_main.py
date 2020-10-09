import os, json

from lef.main import EventType, Extension
from unittest import TestCase
from unittest.mock import patch, call
from tests.utils import FakeResponse


class MainTest(TestCase):
    def setUp(self):
        self.original_env = os.environ
        os.environ = {"AWS_LAMBDA_RUNTIME_API": "testruntimeapi"}

    def tearDown(self):
        os.environ = self.original_env
        self.original_env = None

    @patch("lef.utils.request")
    def test_main(self, mock_request):
        mock_request.Request.return_value = "FakeRequestObject"
        mock_request.urlopen.return_value = FakeResponse(
            json.dumps({"eventType": "INVOKE"}).encode(),
            {"Lambda-Extension-Identifier": "lambda-ext-id"},
        )

        def handler(event):
            assert event == {"eventType": "INVOKE"}

        extension = Extension()
        extension.register([EventType.INVOKE], handler)

        assert extension.runtime_api_endpoint == "testruntimeapi"
        assert [] == mock_request.mock_calls
