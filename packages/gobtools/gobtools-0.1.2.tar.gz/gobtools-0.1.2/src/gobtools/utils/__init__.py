"""
Provides utility classes for HTTP requests and functions for formatting JSON strings.

This package includes:
- Client: A class for sending HTTP requests to a specified base URL.
- json_format: A function for formatting dictionaries as JSON strings with
  customizable options for indentation and key sorting.
"""

from .client import Client
from .json import json_format

__all__ = ["Client", "json_format"]
