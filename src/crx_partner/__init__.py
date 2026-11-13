"""CRX Partner SDK: the Manage API for operators."""

from .client import Manage
from .errors import ApiError, ConfigError, NetworkError
from .webhooks import verify_webhook

__version__ = "0.3.2"

__all__ = ["Manage", "ApiError", "ConfigError", "NetworkError", "verify_webhook", "__version__"]
