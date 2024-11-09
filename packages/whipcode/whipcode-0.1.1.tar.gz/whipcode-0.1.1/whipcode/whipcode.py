"""Python client for Whipcode API"""

# stdlib
import base64
import asyncio

# external
import aiohttp
import requests

# internal
from whipcode.exceptions import RequestError, PayloadBuildError


class ExecutionResult:
    """Object holding the result of a request

    Attributes
    ----------
    stdout, str: The standard output of the execution
    stderr, str: The standard error of the execution
    container_age, float: The age of the container
    timeout, bool: Whether the execution timed out
    status, int: The status code of the request
    detail, str: Additional details if the request failed
    """
    def __init__(self, stdout: str, stderr: str, container_age: float, timeout: bool, status: int, detail: str, rapid: dict = {}):
        """
        Constructor method
        """
        self.stdout = stdout
        self.stderr = stderr
        self.container_age = container_age
        self.timeout = timeout
        self.status = status
        self.detail = detail
        self.rapid = rapid

    def __repr__(self):
        """Return the string representation of the result

        Returns
        -------
        str: The string representation of ExecutionResult
        """
        return (f"ExecutionResult(status={repr(self.status)}, "
                f"stdout={repr(self.stdout)}, "
                f"stderr={repr(self.stderr)}, "
                f"container_age={repr(self.container_age)}, "
                f"timeout={repr(self.timeout)}, "
                f"detail={repr(self.detail)}, "
                f"rapid={repr(self.rapid)})")


class Whipcode:
    """Client

    Parameters
    ----------
    provider, dict, optional: The provider configuration

    Attributes
    ----------
    default_provider, dict:The default provider configuration
    provider, dict: The loaded provider configuration

    Methods
    -------
    rapid_key(key: str):
        Set the RapidAPI key for the client
    run_async(code: str, language: str, args: list = [], timeout: int = 0):
        Make an asynchronous request to the API
    run(code: str, language: str, args: list = [], timeout: int = 0):
        Make a synchronous request to the API
    """
    default_provider = {
        "endpoint": "https://whipcode.p.rapidapi.com/run",
        "headers": {
            "X-RapidAPI-Key": "",
            "X-RapidAPI-Host": "whipcode.p.rapidapi.com"
        },
        "query_injects": [
            {}
        ]
    }

    def __init__(self, provider: dict = default_provider):
        """Constructor method"""
        self.provider = provider

    def rapid_key(self, key: str):
        """Set the RapidAPI key for the client.

        Parameters
        ----------
        key, str: The RapidAPI key
        """
        self.provider["headers"]["X-RapidAPI-Key"] = key

    def _build_payload(self, code: str, language: str | int, args: list, timeout: int) -> dict:
        """[internal] Build the payload for the request"""
        try:
            payload = {
                "code": base64.b64encode(code.encode()).decode(),
                "language_id": str(language),
                "args": " ".join(args),
                "timeout": timeout
            }

            for inject in self.provider["query_injects"]:
                payload.update(inject)

            return payload

        except Exception as e:
            raise PayloadBuildError(e)

    def run_async(self, code: str, language: str | int, args: list = [], timeout: int = 0) -> asyncio.Future:
        """Make an asynchronous request to the API

        Parameters
        ----------
        code, str: The code to execute
        language, str/int: The language ID
        args, list, optional: The arguments to pass to the code
        timeout, int, optional: The timeout for the request

        Returns
        -------
        asyncio.Future: The future object that will resolve to ExecutionResult
        """
        future = asyncio.get_event_loop().create_future()
        asyncio.create_task(self._request_async(code, language, args, timeout, future))
        return future

    async def _request_async(self, code: str, language: str | int, args: list, timeout: int, future: asyncio.Future):
        """[internal] Make the async request to the API"""
        headers = self.provider["headers"]
        payload = self._build_payload(code, language, args, timeout)
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(self.provider["endpoint"], headers=headers, json=payload) as response:
                    json_response = await response.json()
                    result = ExecutionResult(
                        status=response.status,
                        stdout=json_response.get("stdout", ""),
                        stderr=json_response.get("stderr", ""),
                        container_age=json_response.get("container_age", 0),
                        timeout=json_response.get("timeout", False),
                        detail=json_response.get("detail", "")
                    )
                    future.set_result(result)

        except Exception as e:
            future.set_exception(RequestError(e))

    def run(self, code: str, language: str | int, args: list = [], timeout: int = 0) -> ExecutionResult:
        """Make a synchronous request to the API

        Parameters
        ----------
        code, str: The code to execute
        language, str/int: The language ID
        args, list, optional: The arguments to pass to the code
        timeout, int, optional: The timeout for the request

        Returns
        -------
        ExecutionResult: The result of the request
        """
        headers = self.provider["headers"]
        payload = self._build_payload(code, language, args, timeout)
        try:
            response = requests.post(self.provider["endpoint"], headers=headers, json=payload)
            json_response = response.json()
            return ExecutionResult(
                status=response.status_code,
                stdout=json_response.get("stdout", ""),
                stderr=json_response.get("stderr", ""),
                container_age=json_response.get("container_age", 0),
                timeout=json_response.get("timeout", False),
                detail=json_response.get("detail", ""),
                rapid={
                    "messages": json_response.get("messages", ""),
                    "message": json_response.get("message", ""),
                    "info": json_response.get("info", ""),
                }
            )

        except Exception as e:
            raise RequestError(e)
