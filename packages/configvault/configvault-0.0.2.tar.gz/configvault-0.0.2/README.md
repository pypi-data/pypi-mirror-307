# ConfigVault

[![PyPI - Version](https://img.shields.io/pypi/v/configvault?style=for-the-badge)](https://pypi.org/project/configvault)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/configvault?style=for-the-badge)
![GitHub License](https://img.shields.io/github/license/devcoons/configvault?style=for-the-badge)
![PyPI - Wheel](https://img.shields.io/pypi/wheel/configvault?style=for-the-badge&color=%23F0F)

`ConfigVault` is a Python library that provides secure, encrypted configuration storage for sensitive data. It allows you to store, retrieve, and manage configuration settings with ease and security. Perfect for applications that require protected access to configuration details like API keys or database credentials.

## Table of Contents

- [Installation](#installation)
- [Features](#features)
- [Usage](#usage)
  - [Basic Initialization](#basic-initialization)
  - [Storing Configuration](#storing-configuration)
  - [Retrieving Configuration](#retrieving-configuration)
  - [Removing Configurations](#removing-configurations)
- [Security](#security)

## Installation

To use ConfigVault, install it using pip:

```
pip install configvault
```


## Features

- Secure, encrypted storage for sensitive configuration data.
- Supports storing, retrieving, and removing specific configurations by key.
- Option to overwrite existing configurations with @force=True@.
- Ability to clear all stored configurations at once.

## Usage

### Basic Initialization

To get started, initialize `ConfigVault` with a storage folder path and a password for key derivation. A unique, strong password is recommended.

```
from configvault import ConfigVault

vault = ConfigVault(folder_path='path/to/storage', password='my_secure_password')
```


### Storing Configuration

Store a configuration dictionary securely under a specific key. Set `force=True` if you want to overwrite an existing entry.

```
data = {"database": "mydb", "user": "admin", "password": "secure_password"} 
vault.store("db_config", data, force=True) # Overwrites if "db_config" exists
```


### Retrieving Configuration

Retrieve and decrypt stored data by its key.

```
retrieved_data = vault.retrieve("db_config") 
print(retrieved_data) # Output: {"database": "mydb", "user": "admin", "password": "secure_password"}
```


### Removing Configurations

To remove a specific configuration by its key, use the `remove` method.

```
vault.remove("db_config") # Removes the configuration with key "db_config"
```


To remove all stored configurations, use the `remove_all` method:

```
vault.remove_all() # Clears all configurations
```


## Security

ConfigVault uses @cryptography@ for secure encryption based on a key derived from your password. For optimal security:

- Use a strong, unique password.
- Store your password securely (e.g., in an environment variable).
- Set a unique folder path for each application's configurations.

ConfigVault is ideal for applications that need sensitive data management, providing a reliable, encrypted storage solution.
