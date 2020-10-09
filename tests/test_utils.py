from lef.utils import get, post
from unittest import TestCase
from unittest.mock import patch, call
from tests.utils import FakeResponse


class UtilsTest(TestCase):
    @patch("lef.utils.request")
    def test_get(self, mock_request):
        mock_request.Request.return_value = "FakeRequestObject"
        mock_request.urlopen.return_value = FakeResponse("fake response".encode())
        result = get("https://test.com", headers={"test": "header"})

        assert "fake response" == result.text
        assert [
            call.Request(url="https://test.com", headers={"test": "header"}),
            call.urlopen("FakeRequestObject"),
        ] == mock_request.mock_calls

    @patch("lef.utils.request")
    def test_post(self, mock_request):
        mock_request.Request.return_value = "FakeRequestObject"
        mock_request.urlopen.return_value = FakeResponse("fake response".encode())
        result = post(
            "https://test.com", headers={"test": "header"}, data={"key": "value"}
        )

        assert "fake response" == result.text
        assert [
            call.Request(
                url="https://test.com",
                headers={"test": "header", "Content-Type": "application/json"},
                data='{"key": "value"}',
            ),
            call.urlopen("FakeRequestObject"),
        ] == mock_request.mock_calls
