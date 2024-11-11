from getpass import getpass
import rsa
from pathlib import Path
from typing import Tuple, List
from argparse import ArgumentParser

from ..keys.read_key import get_existing_keys, get_public_key_string
from .. import MESSAGE_CHUNK_SIZE, LOGO

def encrypt_command():
    parser = ArgumentParser()
    parser.add_argument("-f", type=str, default=None, 
                        help="Path to file you want to encrypt. Cannot be used with -m")
    parser.add_argument("-o", type=str, default=".", 
                        help="Path to save the encrypted file.")
    parser.add_argument("-m", action='store_true',
                        help="Flag to indicate a message will be provided for encryption. Cannot be used with -f")
    parser.add_argument("-s",  action='store_true',
                        help="Flag to indicate the output should be signed")
    parser.add_argument("-n",  action='store_true', 
                        help="Flag to indicate the output should not be encrypted by a public key. Requires -s to be used.")
    args = parser.parse_args()

    print(LOGO)

    encrypter = GiraffeEncrypter(
        file_path=Path(args.f),
        msg_flag=args.m,
        sign_flag=args.s,
        no_public_key_flag=args.n,
        output_dir=Path(args.o)
    )
    encrypter.encrypt()


class GiraffeEncrypter():

    def __init__(self, file_path: Path = None, msg_flag: bool = False, 
                 sign_flag: bool = False, no_public_key_flag: bool = False,
                 output_dir: Path = Path(".")):
        assert (file_path is None) == msg_flag, "One of -f (--file-path) or -m (--message) must always be passed! Both cannot be used at the same time!"
        if file_path is not None:
            assert file_path.is_file(), "Provided file_path option -f (--file-path) is not a valid File!"
        if no_public_key_flag == True:
            assert sign_flag == True, "Cannot turn off public-key encryption unless -s (--sign) flag is also passed!"
        assert output_dir.is_dir(), f"Save path option -o (--output-dir) is not a valid directory. Got {output_dir.absolute()}"

        self.file_path = file_path
        self.msg_flag = msg_flag
        self.sign_flag = sign_flag
        self.no_public_key_flag = no_public_key_flag
        self.output_dir = output_dir

        _, self.private_key = get_existing_keys()
        if not self.no_public_key_flag:
            self.public_key = get_public_key_string()

    def encrypt(self):
        extension, encrypted_message = self._encrypt()
        self._create_grff_file(encrypted_message, extension)

    def _encrypt(self) -> Tuple[str, bytes]:
        if self.msg_flag:
            msg = getpass("Enter secret: ")
            encrypted_msg = self._encrypt_message(msg.encode())
            extention = None
        else:
            with open(self.file_path, 'rb') as file:
                msg = file.read()
            encrypted_msg = self._encrypt_message(msg)
            extention = self.file_path.suffix
        
        return extention, encrypted_msg
    
    @staticmethod
    def _chunk_message(msg: bytes) -> List[bytes]:
        return [msg[i*MESSAGE_CHUNK_SIZE: (i+1)*MESSAGE_CHUNK_SIZE] 
                    for i in range(len(msg)//MESSAGE_CHUNK_SIZE + 1)]

    def _encrypt_message(self, msg: bytes) -> bytes:
        """Receives string message, returns encrypted message as bytes"""
        chunks = self._chunk_message(msg)
        if not self.no_public_key_flag:
            chunks = [rsa.encrypt(chunk, self.public_key) for chunk in chunks]
        if self.sign_flag:
            chunks = [rsa.sign(chunk, self.private_key) for chunk in chunks]
        return b"".join(chunks)

    def _create_grff_file(self, encrypted_msg: bytes, extension: str) -> None:
        """Writes the encrypted file in the directory"""

        byte_ext = extension.encode() if extension is not None else b''
        byte_ext_size = bytes([len(byte_ext)])
        
        with open(self.output_dir / "secret.grff", 'wb') as file:
            file.write(byte_ext_size)
            if byte_ext != b'':
                file.write(byte_ext)
            file.write(encrypted_msg)


if __name__ == "__main__":
    print(LOGO)
    encrypter = GiraffeEncrypter(
        msg_flag=True
    )
    encrypter.encrypt()

