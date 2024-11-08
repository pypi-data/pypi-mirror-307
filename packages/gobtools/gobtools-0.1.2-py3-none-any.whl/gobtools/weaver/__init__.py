"""
The weaver package manages and interacts with artifacts, releases, and graph data.

This package includes modules and classes for handling HTTP requests and performing
operations related to artifact retrieval, release management, and graph traversal
using specialized controller classes.
"""

from .controller import WeaverController

__all__ = ["WeaverController"]
