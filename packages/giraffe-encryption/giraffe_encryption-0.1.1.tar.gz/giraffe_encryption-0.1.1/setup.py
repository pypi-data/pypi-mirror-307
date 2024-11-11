from setuptools import setup, find_packages

setup(
    name="giraffe_encryption",
    version="0.1.1",
    packages=find_packages(),
    install_requres=[
        "rsa"
    ],
    entry_points={
        "console_scripts": [
            "giraffe-keygen = giraffe_encryption.keys:giraffe_keygen",
            "giraffe-show-key = giraffe_encryption.keys:print_public_key",
            "giraffe-encrypt = giraffe_encryption.encryption.encrypt:encrypt_command"
        ]
    }
)