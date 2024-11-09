# whipcode-py
A convenient way to interact with [Whipcode API](https://whipcode.app) from Python applications.

Compatible with [self-hosted](https://github.com/Whipcode-API/whipcode) instances as well.

## Installation
Get it from PyPI:
```
pip install whipcode
```

## Usage
Here's an asynchronous snippet:
```python
import asyncio

from whipcode import Whipcode

async def main():
    whip = Whipcode()
    whip.rapid_key("YOUR_RAPIDAPI_KEY")

    code = "echo 'Hello World!'"
    lang = 3

    execution = whip.run_async(code, lang)
    result = await execution

    print(result)

asyncio.run(main())
```
And a synchronous one:
```python
from whipcode import Whipcode

def main():
    whip = Whipcode()
    whip.rapid_key("YOUR_RAPIDAPI_KEY")

    code = "echo 'Hello World!'"
    lang = 3

    result = whip.run(code, lang)

    print(result)

main()
```
The output:
```
ExecutionResult(status=200, stdout='Hello World!\n', stderr='', container_age=0.338638005, timeout=False, detail='', rapid={'messages': '', 'message': '', 'info': ''})
```

## Providers
Changing the provider is easy. Here's how the default provider is defined:
```python
{
  "endpoint": "https://whipcode.p.rapidapi.com/run",
  "headers": {
    "X-RapidAPI-Key": "",
    "X-RapidAPI-Host": "whipcode.p.rapidapi.com"
  },
  "query_injects": [
    {}
  ]
}
```

Just pass your custom provider to the constructor:
```python
whip = Whipcode(custom_provider)
```

Or swap it in on the already initialized object:
```python
whip.provider = custom_provider
```

An example custom provider:
```python
{
  "endpoint": "https://<host>/run",
  "headers": {
    "Authorization": "Bearer xxx"
  },
  "query_injects": []
}
```

## Reference
### Constructor
```python
Whipcode(provider: dict = Whipcode.default_provider)
```
**Parameters:**
- **provider** - *dict, optional*\
  &nbsp;&nbsp;&nbsp;The provider configuration. See the [Providers](#providers) section.

### rapid_key
```python
rapid_key(key: str)
```
Sets the RapidAPI key to use when making requests.

**Parameters:**
- **key** - *str*\
  &nbsp;&nbsp;&nbsp;Your RapidAPI key.

### run
```python
run(code: str, language_id: str | int, args: list = [], timeout: int = 0) -> ExecutionResult
```
Makes a request to the endpoint synchronously.

**Parameters:**
- **code** - *str*\
  &nbsp;&nbsp;&nbsp;The code to execute.
- **language_id** - *str, int*\
  &nbsp;&nbsp;&nbsp;Language ID of the submitted code.
- **args** - *list, optional*\
  &nbsp;&nbsp;&nbsp;A list of compiler/interpreter args.
- **timeout** - *int, optional*\
  &nbsp;&nbsp;&nbsp;Timeout in seconds for the code to run.

**Returns:**
- [ExecutionResult](#executionresult)

### run_async
```python
run_async(code: str, language_id: str | int, args: list = [], timeout: int = 0) -> asyncio.Future
```
Makes a request to the endpoint asynchronously.

**Parameters:**
- **code** - *str*\
  &nbsp;&nbsp;&nbsp;The code to execute.
- **language_id** - *str, int*\
  &nbsp;&nbsp;&nbsp;Language ID of the submitted code.
- **args** - *list, optional*\
  &nbsp;&nbsp;&nbsp;A list of compiler/interpreter args.
- **timeout** - *int, optional*\
  &nbsp;&nbsp;&nbsp;Timeout in seconds for the code to run.

**Returns:**
- A future that resolves to [ExecutionResult](#executionresult).

### ExecutionResult
```python
ExecutionResult(stdout: str, stderr: str, container_age: float, timeout: bool, status: int, detail: str, rapid: dict = {})
```
Returned as the result after a request.

**Attributes**
- **stdout** - *str*\
  &nbsp;&nbsp;&nbsp;All data captured from stdout.
- **stderr** - *str*\
  &nbsp;&nbsp;&nbsp;All data captured from stderr.
- **container_age** - *float*\
  &nbsp;&nbsp;&nbsp;Duration the container allocated for your code ran, in seconds.
- **timeout** - *bool*\
  &nbsp;&nbsp;&nbsp;Boolean value depending on whether your container lived past the timeout period.
- **status** - *int*\
  &nbsp;&nbsp;&nbsp;The status code of the request response.
- **detail** - *str*\
  &nbsp;&nbsp;&nbsp;Details about why the request failed to complete.
- **rapid** - *dict*\
  &nbsp;&nbsp;&nbsp;Various keys that RapidAPI uses when returning their own error messages.

### Exceptions
- **RequestError** - Raised when an error occurs during the request
- **PayloadBuildError** - Raised when an error occurs while building the payload

## Contributing
Please read the [contributing guidelines](https://github.com/Whipcode-API/whipcode-py/blob/main/.github/CONTRIBUTING.md) before opening a pull request.

## License
This library is licensed under the [MIT License](https://github.com/Whipcode-API/whipcode-py/blob/main/LICENSE).
