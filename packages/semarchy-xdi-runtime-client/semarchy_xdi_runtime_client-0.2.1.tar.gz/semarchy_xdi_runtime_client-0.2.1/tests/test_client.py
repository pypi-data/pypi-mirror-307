import json
from unittest import mock
from semarchy_xdi_runtime_client.client.client import (
    XDIApiClient,
    XDIRuntimeStatus,
)


class TestSemarchyXDIRuntimeClient:
    @mock.patch(
        "semarchy_xdi_runtime_client.client.client.PreparedRequest.run"
    )
    def test_get_runtime_status(self, mock_post: mock.MagicMock):
        client = XDIApiClient(runtime_host="https://dummy.debug")
        mock_post.return_value = mock.MagicMock(status_code=200, text="true")

        assert client.get_runtime_status() == XDIRuntimeStatus.RUNNING

    @mock.patch(
        "semarchy_xdi_runtime_client.client.client.PreparedRequest.run"
    )
    def test_launch_delivery(self, mock_post: mock.MagicMock):
        SESSION_ID = "2c323aec4c473dae83"
        client = XDIApiClient(runtime_host="https://dummy.debug")
        response = {"singleResult": f"sessionid:{SESSION_ID}"}
        mock_post.return_value = mock.MagicMock(
            status_code=200, text=json.dumps(response)
        )

        assert (
            client.launch_delivery(
                job_name="TEST_JOB_NAME", job_vars="var ~/TestVariable"
            )
            == SESSION_ID
        )
