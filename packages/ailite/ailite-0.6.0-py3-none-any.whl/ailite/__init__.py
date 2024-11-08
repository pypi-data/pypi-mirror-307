"""
This module provides the main interfaces for the ailite package.
"""

# Import the specific classes
from ailite._model._api import HUGPiLLM, HUGPIClient
from ailite.main._ailite import ai, ClaudeEngine

# Define what should be exposed when using "from ailite import *"
__all__ = [
    'ai',
    'HUGPIClient',
    'HUGPiLLM',
    'ClaudeEngine'
]

# Optionally, you can add version info
__version__ = '0.5.0'