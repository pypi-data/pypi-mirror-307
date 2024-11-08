# FPBase Client

A Python client for the FPBase REST API.

## Overview

FPBase Client is a Python package that provides a convenient interface to the FPBase REST API. It allows you to:

- Retrieve protein information
- Search for proteins
- Cache results locally
- Handle rate limiting automatically

## Quick Start

```python
from fpbase_client import FPBaseAPI

# Initialize the client
client = FPBaseAPI()

# Get a specific protein
protein = client.get_protein("egfp")

# Get all proteins
proteins = client.get_all_proteins() # returns a generator of protein objects
```

## Features

- Simple and intuitive API
- Automatic rate limiting
- Local caching support
- Comprehensive error handling

