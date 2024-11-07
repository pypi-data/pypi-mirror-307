import os
import argparse
import sys
from typing import Optional

class JuiceFSClient:
    """
    A client class for JuiceFS operations that can be easily integrated into other Python projects.
    
    Environment Variables:
        JUICEFS_VOLUME: JuiceFS volume name
        JUICEFS_TOKEN: JuiceFS authentication token
        AWS_ACCESS_KEY_ID: AWS access key ID
        AWS_SECRET_ACCESS_KEY: AWS secret access key
    
    Example usage:
        # Using environment variables
        export JUICEFS_VOLUME=myvolume
        export JUICEFS_TOKEN=mytoken
        export AWS_ACCESS_KEY_ID=AKIAXXXXXXXXXXXXXXXX
        export AWS_SECRET_ACCESS_KEY=XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
        client = JuiceFSClient()
    """
    
    def __init__(self, volume: Optional[str] = None, token: Optional[str] = None, 
                 access_key: Optional[str] = None, secret_key: Optional[str] = None):
        """
        Initialize JuiceFS client with authentication details.
        If parameters are not provided, will attempt to read from environment variables.
        
        Args:
            volume (str, optional): JuiceFS volume name
            token (str, optional): JuiceFS authentication token
            access_key (str, optional): AWS access key ID
            secret_key (str, optional): AWS secret access key
            
        Raises:
            ValueError: If required credentials are not provided via parameters or environment variables
        """
        # Get credentials from environment variables or parameters
        self.volume = volume or os.environ.get('JUICEFS_VOLUME')
        self.token = token or os.environ.get('JUICEFS_TOKEN')
        self.access_key = access_key or os.environ.get('AWS_ACCESS_KEY_ID')
        self.secret_key = secret_key or os.environ.get('AWS_SECRET_ACCESS_KEY')
        
        # Validate credentials
        missing = []
        for name, value, env_var in [
            ('volume', self.volume, 'JUICEFS_VOLUME'),
            ('token', self.token, 'JUICEFS_TOKEN'),
            ('access_key', self.access_key, 'AWS_ACCESS_KEY_ID'),
            ('secret_key', self.secret_key, 'AWS_SECRET_ACCESS_KEY')
        ]:
            if not value:
                missing.append(f"{name} ({env_var})")
        
        if missing:
            error_msg = (
                f"Missing required credentials: {', '.join(missing)}.\n\n"
                "Please provide credentials in one of these ways:\n\n"
                "1. Using environment variables:\n"
                "   export JUICEFS_VOLUME=myvolume\n"
                "   export JUICEFS_TOKEN=mytoken\n"
                "   export AWS_ACCESS_KEY_ID=AKIAXXXXXXXXXXXXXXXX\n"
                "   export AWS_SECRET_ACCESS_KEY=XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX\n\n"
                "2. Using parameters when creating the client:\n"
                "   client = JuiceFSClient(\n"
                "       volume='myvolume',\n"
                "       token='mytoken',\n"
                "       access_key='AKIAXXXXXXXXXXXXXXXX',\n"
                "       secret_key='XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'\n"
                "   )\n\n"
                "3. Using command line arguments:\n"
                "   python bind.py --volume myvolume --token mytoken \\\n"
                "                 --access-key AKIAXXXXXXXXXXXXXXXX \\\n"
                "                 --secret-key XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX \\\n"
                "                 mount /path/to/mount"
            )
            raise ValueError(error_msg)
        
        self.juicefs = self._check_juicefs_installation()
        self.client = self.juicefs.Client(
            self.volume,
            token=self.token,
            access_key=self.access_key,
            secret_key=self.secret_key
        )

    @staticmethod
    def _check_juicefs_installation():
        """
        Ensure JuiceFS is installed. If pip is not available, install it using curl.
        
        Returns:
            module: The juicefs module
            
        Raises:
            RuntimeError: If installation fails
        """
        try:
            import juicefs
            return juicefs
        except ImportError:
            print("JuiceFS not found. Checking pip installation...")
            
            import subprocess
            import sys
            import tempfile
            
            # Check if pip is available
            try:
                subprocess.check_call([sys.executable, "-m", "pip", "--version"], 
                                   stdout=subprocess.DEVNULL, 
                                   stderr=subprocess.DEVNULL)
            except (subprocess.CalledProcessError, FileNotFoundError):
                print("pip not found. Installing pip first...")
                try:
                    # Create a temporary directory for get-pip.py
                    with tempfile.TemporaryDirectory() as tmp_dir:
                        # Download get-pip.py
                        subprocess.check_call([
                            "curl", "-sSL", 
                            "https://bootstrap.pypa.io/get-pip.py",
                            "-o", f"{tmp_dir}/get-pip.py"
                        ])
                        # Install pip
                        subprocess.check_call([sys.executable, f"{tmp_dir}/get-pip.py"])
                except subprocess.CalledProcessError as e:
                    raise RuntimeError(
                        "Failed to install pip. Please install pip manually:\n"
                        "curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py && "
                        f"{sys.executable} get-pip.py"
                    )
            
            # Now install JuiceFS
            try:
                print("Installing JuiceFS...")
                subprocess.check_call([
                    sys.executable,
                    "-m",
                    "pip",
                    "install",
                    "https://static.juicefs.com/misc/juicefs-5.1.1-py3-none-any.whl"
                ])
                
                print("\n" + "="*60)
                print("JuiceFS has been installed successfully!")
                print("Please rerun your command to continue.")
                print("="*60 + "\n")
                sys.exit(0)
                
            except Exception as e:
                raise RuntimeError(
                    f"Failed to install JuiceFS: {str(e)}\n"
                    "Please try installing it manually:\n"
                    f"{sys.executable} -m pip install "
                    "https://static.juicefs.com/misc/juicefs-5.1.1-py3-none-any.whl"
                )

    def mount(self, path: str) -> None:
        """
        Mount a JuiceFS directory.
        
        Args:
            path (str): Local path where the JuiceFS directory will be mounted
        """
        self.client.makedirs(path)
        print(f"Successfully mounted JuiceFS at {path}")

    def write_file(self, path: str, content: str) -> None:
        """
        Write content to a file in JuiceFS.
        
        Args:
            path (str): Path to the file in JuiceFS
            content (str): Content to write to the file
        """
        with self.client.open(path, "w") as f:
            f.write(content)
        print(f"Successfully wrote to {path}")

    def read_file(self, path: str) -> str:
        """
        Read content from a file in JuiceFS.
        
        Args:
            path (str): Path to the file in JuiceFS
            
        Returns:
            str: Content of the file
        """
        with self.client.open(path) as f:
            return f.read()

    def delete_file(self, path: str) -> None:
        """
        Delete a file from JuiceFS.
        
        Args:
            path (str): Path to the file to delete in JuiceFS
        """
        self.client.remove(path)
        print(f"Successfully deleted {path}")

    def write_binary(self, path: str, content: bytes) -> None:
        """
        Write binary content to a file in JuiceFS.
        
        Args:
            path (str): Path to the file in JuiceFS
            content (bytes): Binary content to write to the file
            
        Example:
            # Save a PyTorch model
            model_state = model.state_dict()
            buffer = io.BytesIO()
            torch.save(model_state, buffer)
            client.write_binary('/path/to/model.pt', buffer.getvalue())
        """
        with self.client.open(path, "wb") as f:
            f.write(content)
        print(f"Successfully wrote binary data to {path}")

    def read_binary(self, path: str) -> bytes:
        """
        Read binary content from a file in JuiceFS.
        
        Args:
            path (str): Path to the file in JuiceFS
            
        Returns:
            bytes: Binary content of the file
            
        Example:
            # Load a PyTorch model
            model_data = client.read_binary('/path/to/model.pt')
            buffer = io.BytesIO(model_data)
            model.load_state_dict(torch.load(buffer))
        """
        with self.client.open(path, "rb") as f:
            return f.read()

    def save_torch_model(self, path: str, model_state: dict) -> None:
        """
        Save a PyTorch model state dict to JuiceFS.
        
        Args:
            path (str): Path to save the model file in JuiceFS
            model_state: PyTorch model state dict
            
        Example:
            client.save_torch_model('/path/to/model.pt', model.state_dict())
        """
        import io
        import torch
        
        buffer = io.BytesIO()
        torch.save(model_state, buffer)
        self.write_binary(path, buffer.getvalue())

    def load_torch_model(self, path: str) -> dict:
        """
        Load a PyTorch model state dict from JuiceFS.
        
        Args:
            path (str): Path to the model file in JuiceFS
            
        Returns:
            dict: PyTorch model state dict
            
        Example:
            model_state = client.load_torch_model('/path/to/model.pt')
            model.load_state_dict(model_state)
        """
        import io
        import torch
        
        binary_data = self.read_binary(path)
        buffer = io.BytesIO(binary_data)
        return torch.load(buffer)

def main():
    """CLI interface for JuiceFS operations"""
    parser = argparse.ArgumentParser(
        description='''
JuiceFS CLI Operations - A simple tool to interact with JuiceFS

Credentials can be provided via command line arguments or environment variables:
    JUICEFS_VOLUME: JuiceFS volume name
    JUICEFS_TOKEN: JuiceFS authentication token
    AWS_ACCESS_KEY_ID: AWS access key ID
    AWS_SECRET_ACCESS_KEY: AWS secret access key

Examples:
    # Using environment variables:
    export JUICEFS_VOLUME=myvolume
    export JUICEFS_TOKEN=mytoken
    export AWS_ACCESS_KEY_ID=AKIAXXXXXXXXXXXXXXXX
    export AWS_SECRET_ACCESS_KEY=XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
    python bind.py mount /path/to/mount
''',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    # Common arguments (now optional if env vars are set)
    parser.add_argument('--volume', help='JuiceFS volume name (env: JUICEFS_VOLUME)')
    parser.add_argument('--token', help='JuiceFS authentication token (env: JUICEFS_TOKEN)')
    parser.add_argument('--access-key', help='AWS access key ID (env: AWS_ACCESS_KEY_ID)')
    parser.add_argument('--secret-key', help='AWS secret access key (env: AWS_SECRET_ACCESS_KEY)')

    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # Mount command
    mount_parser = subparsers.add_parser('mount', 
        help='Mount a JuiceFS directory',
        description='Create and mount a directory in JuiceFS filesystem')
    mount_parser.add_argument('path', help='Local path where the JuiceFS directory will be mounted')

    # Write command
    write_parser = subparsers.add_parser('write',
        help='Write content to a file',
        description='Write specified content to a file in JuiceFS filesystem')
    write_parser.add_argument('path', help='Path to the file in JuiceFS')
    write_parser.add_argument('content', help='Content to write to the file')

    # Read command
    read_parser = subparsers.add_parser('read',
        help='Read file content',
        description='Read and display content of a file from JuiceFS filesystem')
    read_parser.add_argument('path', help='Path to the file in JuiceFS')

    # Delete command
    delete_parser = subparsers.add_parser('delete',
        help='Delete a file',
        description='Remove a file from JuiceFS filesystem')
    delete_parser.add_argument('path', help='Path to the file to delete in JuiceFS')

    args = parser.parse_args()
    
    # Create client instance
    client = JuiceFSClient(args.volume, args.token, args.access_key, args.secret_key)

    # Execute commands
    if args.command == 'mount':
        client.mount(args.path)
    elif args.command == 'write':
        client.write_file(args.path, args.content)
    elif args.command == 'read':
        print(client.read_file(args.path))
    elif args.command == 'delete':
        client.delete_file(args.path)
    else:
        parser.print_help()
        sys.exit(1)

if __name__ == "__main__":
    main()