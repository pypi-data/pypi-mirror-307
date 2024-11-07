import os
from cryptography.fernet import Fernet

KEY_FILE_PATH = os.path.join(os.path.dirname(__file__), ".dart_key")


def get_or_create_dart_key():
    """
    Checks for the existence of the encryption key. Generates and saves a new key if not found.
    Loads the key into the environment as DART_KEY.
    """
    # Check if key file exists
    if os.path.exists(KEY_FILE_PATH):
        # Load the existing key from the file
        with open(KEY_FILE_PATH, "rb") as key_file:
            key = key_file.read()
    else:
        # Generate a new key and save it to the key file
        key = Fernet.generate_key()
        with open(KEY_FILE_PATH, "wb") as key_file:
            key_file.write(key)

    # Set the key as an environment variable for use in the application
    os.environ["DART_KEY"] = key.decode()
    return key
