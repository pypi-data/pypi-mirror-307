# CIFAR-10 Client

A Python client for interacting with the CIFAR-10 image classification API.

## Installation

```bash
pip install cifar10-client
```

## Quick Start

```python
from cifar10_client import CIFAR10Client

# Initialize client
client = CIFAR10Client("http://your-api-url:5000")

# Single prediction
result = client.predict_single("path/to/image.jpg")
print(f"Prediction: {result['prediction']} ({result['confidence']}%)")

# Top 3 predictions
result = client.predict_top3("path/to/image.jpg")
for pred, conf in zip(result['predictions'], result['confidences']):
    print(f"{pred}: {conf}%")

# Batch prediction
results = client.predict_batch(["image1.jpg", "image2.jpg"])
for item in results['results']:
    print(f"\nFile: {item['filename']}")
    for pred, conf in zip(item['predictions'], item['confidences']):
        print(f"{pred}: {conf}%")
```

## CLI Usage

```bash
# Single prediction
cifar10-predict image.jpg

# Top 3 predictions
cifar10-predict --top3 image.jpg

# Batch prediction
cifar10-predict --batch image1.jpg image2.jpg image3.jpg
```