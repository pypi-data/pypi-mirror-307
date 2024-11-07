# src/cifar10_client/client.py
import requests
from typing import List, Dict, Union
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

class CIFAR10Client:
    """Client for interacting with the CIFAR-10 classification API."""
    
    DEFAULT_URL = "http://16.171.55.173:5000"
    
    def __init__(self, base_url: str = DEFAULT_URL, timeout: int = 30):
        """
        Initialize the client with the API's base URL.
        
        Args:
            base_url (str): Base URL of the API (defaults to class DEFAULT_URL)
            timeout (int): Request timeout in seconds
        """
        self.base_url = base_url.rstrip('/')
        self.timeout = timeout