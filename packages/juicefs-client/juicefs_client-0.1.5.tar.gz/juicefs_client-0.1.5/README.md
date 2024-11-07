# JuiceFS Client

A Python client for JuiceFS operations with easy-to-use interfaces and AWS credentials support.

## Installation

```bash
pip install juicefs-client
```

## Quick Start

### Initialize Client

```python
from juicefs_client import JuiceFSClient

# Using environment variables (AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY)
client = JuiceFSClient(volume="myvolume", token="mytoken")

# Or with explicit credentials
client = JuiceFSClient(
    volume="myvolume",
    token="mytoken",
    access_key="your-aws-access-key",
    secret_key="your-aws-secret-key"
)
```

### Basic File Operations

```python
# Write and read text files
client.write_file("/path/to/file.txt", "Hello World")
content = client.read_file("/path/to/file.txt")

# Binary files (e.g., PyTorch models)
client.save_torch_model("/models/model.pt", model.state_dict())
state_dict = client.load_torch_model("/models/model.pt")

# List directory contents
files = client.list_dir("/path/to/directory")

# Delete files
client.delete_file("/path/to/file.txt")

# Copy files
client.copy_file("/source/path", "/destination/path")
```

## Features

- Simple and intuitive API for JuiceFS operations
- AWS credentials support (both environment variables and explicit)
- Built-in support for PyTorch model serialization
- File operations: read, write, delete, copy, list
- Directory operations: create, list, delete

## Configuration

| Parameter | Description | Required | Default |
|-----------|-------------|----------|----------|
| volume | JuiceFS volume name | Yes | None |
| token | Authentication token | Yes | None |
| access_key | AWS access key | No | None |
| secret_key | AWS secret key | No | None |
| endpoint | Custom endpoint URL | No | None |
| region | AWS region | No | 'us-east-1' |

## Error Handling

```python
from juicefs_client.exceptions import JuiceFSError

try:
    client.read_file("/nonexistent/file.txt")
except JuiceFSError as e:
    print(f"Error: {e}")
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.