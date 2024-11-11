# config_encryptor/key_manager.py

import os
from cryptography.fernet import Fernet
import subprocess

def generate_key(file_path='secret.key'):
    """
    Generate and store an encryption key in a file.
    """
    key = Fernet.generate_key()
    os.environ['CONFIG_ENCRYPTION_KEY'] = key.decode()
    set_permanent_env_var('CONFIG_ENCRYPTION_KEY', key)
    return key

def load_key():
    """
    Load the encryption key from an environment variable or file.
    """
    key = os.getenv('CONFIG_ENCRYPTION_KEY')

    if key:
        return key.encode()
    else:
       raise ValueError("No encryption key found in environment")
def set_permanent_env_var(var_name, var_value):
    """
    Sets a permanent environment variable on Windows using the 'setx' command.
    """
    try:
        # Use the setx command to permanently set the environment variable
        subprocess.run(['setx', var_name, var_value], check=True)
        print(f"Environment variable '{var_name}' set successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Failed to set environment variable: {e}")