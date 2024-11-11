# Config Encryptor

`encryption` is a Python package designed to encrypt and decrypt JSON configuration files, specifically `config.json`, to enhance security for sensitive data such as API keys and database credentials.

## Purpose:
Most developers store their sensitive information in a JSON file which often leads to security threats. This package encrypt the configuration file and decrypt it before using it using a secret key. The secret key is stored in environment variable making it inaccessible to hackers.

## Features:
- Generate an encryption key.
- Encrypt the entire `config.json` file.
- Decrypt the encrypted file for runtime use.

## Installation

```bash
pip install config_encryptor
