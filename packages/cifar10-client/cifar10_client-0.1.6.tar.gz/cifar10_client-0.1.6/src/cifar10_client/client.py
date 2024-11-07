import requests
from typing import List, Dict, Union
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

class CIFAR10Client:
    """Client for interacting with the CIFAR-10 classification API."""
    
    DEFAULT_URL = "http://16.171.55.173:5000"
    
    def __init__(self, base_url: str = DEFAULT_URL, timeout: int = 30):
        """Initialize the client with the API's base URL."""
        self.base_url = base_url.rstrip('/')
        self.timeout = timeout
        
    def predict_single(self, image_path: Union[str, Path]) -> Dict:
        """Get prediction for a single image."""
        with open(image_path, 'rb') as f:
            files = {'file': f}
            response = requests.post(
                f"{self.base_url}/api/predict",
                files=files,
                timeout=self.timeout
            )
            response.raise_for_status()
            return response.json()
    
    def predict_top3(self, image_path: Union[str, Path]) -> Dict:
        """Get top 3 predictions for a single image."""
        with open(image_path, 'rb') as f:
            files = {'file': f}
            response = requests.post(
                f"{self.base_url}/api/predict_top3",
                files=files,
                timeout=self.timeout
            )
            response.raise_for_status()
            return response.json()
    
    def predict_batch(self, image_paths: List[Union[str, Path]]) -> Dict:
        """Get predictions for multiple images."""
        files = [
            ('files', open(path, 'rb')) 
            for path in image_paths
        ]
        try:
            response = requests.post(
                f"{self.base_url}/api/predict_batch",
                files=files,
                timeout=self.timeout
            )
            response.raise_for_status()
            return response.json()
        finally:
            for _, f in files:
                f.close()