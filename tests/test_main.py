import os, json

from lef.main import EventType, Extension
from unittest import TestCase
from unittest.mock import MagicMock, patch, call
from tests.utils import FakeResponse
import pytest

class MainTest(TestCase):
    def setUp(self):
        self.original_env = os.environ
        os.environ = {"AWS_LAMBDA_RUNTIME_API": "testruntimeapi"}

    def tearDown(self):
        os.environ = self.original_env
        self.original_env = None

    @patch('lef.main.post')
    @patch("lef.main.get")
    def test_main(self, mock_get, mock_post):
        mock_get.side_effect = [
            FakeResponse(
                json.dumps({"eventType": "INVOKE"})
            ),
            FakeResponse(
                json.dumps({"eventType": "SHUTDOWN"})
            )
        ]

        mock_post.side_effect = [
            FakeResponse(
                '',
                {"Lambda-Extension-Identifier": "lambda-ext-id"}
            ),
        ]

        handler = MagicMock()
        extension = Extension()

        with pytest.raises(SystemExit) as e:
            extension.register([EventType.INVOKE], handler)

        assert extension.runtime_api_endpoint == "testruntimeapi"
        assert [
            call({'eventType': 'INVOKE'})
        ] == handler.mock_calls
        assert [
            call(url='https://testruntimeapi/2020-01-01/extension/event/next', headers={'Lambda-Extension-Identifier': 'lambda-ext-id'}),
            call(url='https://testruntimeapi/2020-01-01/extension/event/next', headers={'Lambda-Extension-Identifier': 'lambda-ext-id'})
        ] == mock_get.mock_calls
        assert [
            call(url='https://testruntimeapi/2020-01-01/extension/register', data={'events': ['EventType.INVOKE']}, headers={'Lambda-Extension-Name': 'lef'})
        ] == mock_post.mock_calls
