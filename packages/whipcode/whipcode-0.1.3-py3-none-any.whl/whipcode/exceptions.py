"""
Exceptions
---------
RequestError: Raised when an error occurs during the request
PayloadBuildError: Raised when an error occurs while building the payload
"""


class RequestError(Exception):
    """Raised when an error occurs during the request"""
    pass


class PayloadBuildError(Exception):
    """Raised when an error occurs while building the payload"""
    pass
