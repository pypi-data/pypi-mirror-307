# setup.py

# setup.py

from setuptools import setup, find_packages

setup(
    name='config-encryptor',                # Your package name
    version='1.1.0',                        # Version of your package
    description='A Python package for encrypting and decrypting config files using Fernet encryption.',
    long_description=open('README.md').read(),  # Project description (README.md)
    long_description_content_type='text/markdown',  # Markdown format for long description
    author='Shabir Ahmad',                   # Your name
    author_email='shabir@caimy.co.kr',   # Your email
    url='https://github.com/shabir/configencrypt',  # Your project URL (GitHub, etc.)
    packages=find_packages(),               # Automatically find and include all Python packages
    install_requires=[                      # External dependencies for your package
        'cryptography>=3.4.7',
    ],
    classifiers=[                           # Metadata about the package
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',  # Choose your license
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',                # Specify Python version compatibility
)
