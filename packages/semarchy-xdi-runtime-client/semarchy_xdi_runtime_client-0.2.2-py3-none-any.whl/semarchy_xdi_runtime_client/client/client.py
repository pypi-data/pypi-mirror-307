import json
import requests
from urllib.parse import urlparse, ParseResult, urljoin
from typing import Optional
from semarchy_xdi_runtime_client.client import exceptions
from semarchy_xdi_runtime_client.client.helpers import (
    LoggingMixin,
    PreparedRequest,
)
from semarchy_xdi_runtime_client.client.enum import XDIRuntimeStatus


class XDIApiClient(LoggingMixin):
    def __init__(
        self,
        *,
        runtime_host: str,
        verify_host: Optional[bool] = True,
    ) -> None:
        """Initialize the client

        Args:
            runtime_host (str): the XDI runtime host to connect to
            verify_host (Optional[bool], optional): Verify the SSL certs of the runtime. Defaults to True.
        """
        super().__init__()
        self.runtime_host: ParseResult = urlparse(runtime_host)
        self.verify_host = verify_host
        self.session = requests.Session()

    @property
    def client_endpoint(self):
        return urljoin(self.runtime_host.geturl(), "/client/1")

    def get_runtime_status(self) -> XDIRuntimeStatus:
        payload = {
            "parametersTypes": [],
            "method": "isConnected",
        }
        try:
            status = PreparedRequest(
                session=self.session,
                url=self.client_endpoint,
                method="POST",
                payload=payload,
                verify_host=self.verify_host,
            ).run()
        except requests.RequestException as e:
            print(e)
        try:
            return XDIRuntimeStatus(status.text)
        except ValueError:
            raise exceptions.XDIRuntimeUnavailable(
                "runtime did not returned a correct status value"
            )

    def launch_delivery(
        self, job_name: str, job_vars: Optional[str | list[dict[str, str]]]
    ) -> str:
        """Launch delivery

        Args:
            job_name (str): the delivery name
            job_vars (Optional[str  |  list[dict[str, str]]]): the vars to pass to the delivery

        Raises:
            InvalidJobVarsError: The job vars are not correctly formatted
            LaunchJobError: An error occured during the job launch

        Returns:
            str: the session id of the delivery
        """
        computed_job_vars = ""
        if isinstance(job_vars, str):
            computed_job_vars = job_vars
        elif isinstance(job_vars, list):
            computed_job_vars = " ".join(
                [
                    f"var ~/{param['name']} {param['value']}"
                    for param in job_vars
                ]
            )
        else:
            raise exceptions.InvalidJobVarsError
        launch_command = f'execute delivery {job_name} {computed_job_vars} format "session_id:%id"'
        self.log.debug(f"launching command {launch_command}")
        payload = {
            "parametersTypes": ["java.util.Map"],
            "method": "invokeCommand",
            "params": [{"singleCommand": launch_command}],
        }
        try:
            launch = PreparedRequest(
                session=self.session,
                url=self.client_endpoint,
                method="POST",
                payload=payload,
                verify_host=self.verify_host,
            ).run()
        except requests.exceptions.RequestException:
            self.log.error("error while making api call to xdi runtime")
            raise exceptions.LaunchJobError
        try:
            launch_body = launch.text
            session_id: str = (json.loads(launch_body.replace("\n", "")))[
                "singleResult"
            ].split(":")[1]  # retreive session if from string
            return session_id
        except json.JSONDecodeError as json_err:
            self.log.error(
                "error while unmarshalling XDI JSON launch request response"
            )
            self.log.error(json_err)
