import io
import os
import shutil
import struct
import math
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5
import chacha
import re
import base64

# RSA
RSA_KEY_SIZE = 256

# ChaCha20/8
CHACHA_KEY_SIZE = 32
CHACHA_NONCE_SIZE = 8
CHACHA_ROUNDS = 8

# Metadata
ENC_MARKER = b'\x66\x11\x61\x66'

METADATA_SIZE = RSA_KEY_SIZE + 4 + len(ENC_MARKER)

BLOCK_SIZE = 0x10000

SENTINEL_SIZE = 16

PrivateBinPath = 'private.bin'


def rsa_construct_blob(blob):
    """Construct RSA key from BLOB"""
    is_private = False

    type_ver, key_alg, magic, key_bitlen = struct.unpack_from('<4L', blob, 0)
    # "RSA2"
    if (type_ver == 0x207) and (key_alg == 0xA400) and (magic == 0x32415352):
        is_private = True
    # "RSA1"
    elif (type_ver != 0x206) or (key_alg != 0xA400) or (magic != 0x31415352):
        raise ValueError('Invalid RSA blob')

    pos = 16
    key_len = math.ceil(key_bitlen / 8)

    e = int.from_bytes(blob[pos: pos + 4], byteorder='little')
    pos += 4
    n = int.from_bytes(blob[pos: pos + key_len], byteorder='little')

    if not is_private:
        return RSA.construct((n, e))

    key_len2 = math.ceil(key_bitlen / 16)

    pos += key_len
    p = int.from_bytes(blob[pos: pos + key_len2], byteorder='little')
    pos += key_len2
    q = int.from_bytes(blob[pos: pos + key_len2], byteorder='little')
    pos += key_len2
    dp = int.from_bytes(blob[pos: pos + key_len2], byteorder='little')
    pos += key_len2
    dq = int.from_bytes(blob[pos: pos + key_len2], byteorder='little')
    pos += key_len2
    iq = int.from_bytes(blob[pos: pos + key_len2], byteorder='little')
    pos += key_len2
    d = int.from_bytes(blob[pos: pos + key_len], byteorder='little')

    if (dp != d % (p - 1)) or (dq != d % (q - 1)):
        raise ValueError('Invalid RSA blob')

    return RSA.construct((n, e, d, p, q))


def decrypt_file(filename, priv_key):
    """Decrypt file"""
    with io.open(filename, 'rb+') as f:
        # Read metadata
        try:
            f.seek(-METADATA_SIZE, 2)
        except OSError:
            return False

        metadata = f.read(METADATA_SIZE)

        # Check metadata marker
        if metadata[-len(ENC_MARKER):] != ENC_MARKER:
            return False

        # Decrypt ChaCha20 key and nonce
        cipher = PKCS1_v1_5.new(priv_key)

        sentinel = os.urandom(SENTINEL_SIZE)
        enc_key_data = metadata[:RSA_KEY_SIZE]
        key_data = cipher.decrypt(enc_key_data[::-1], sentinel)
        if key_data == sentinel:
            return False

        key = key_data[:CHACHA_KEY_SIZE]
        nonce = key_data[CHACHA_KEY_SIZE:
                         CHACHA_KEY_SIZE + CHACHA_NONCE_SIZE]

        # Remove metadata
        f.seek(-METADATA_SIZE, 2)
        f.truncate()

        cipher = chacha.ChaCha(key, nonce, 0, CHACHA_ROUNDS)

        f.seek(0)

        while True:
            enc_data = f.read(BLOCK_SIZE)
            if enc_data == b'':
                break

            data = cipher.decrypt(enc_data)

            f.seek(-len(enc_data), 1)
            f.write(data)

    return True


def extract_between_markers(input_string, start_marker, end_marker):
    # pattern = re.compile(f'{re.escape(start_marker)}\s*(.*?)\s*{re.escape(end_marker)}', re.DOTALL | re.IGNORECASE)
    pattern = re.compile(f'{re.escape(start_marker)}\s(.*?)\s{re.escape(end_marker)}', re.DOTALL | re.IGNORECASE)
    match = pattern.search(input_string)
    stIndex = input_string.find("KEY")
    lsIndex = input_string.find("---END")
    print(input_string)
    if stIndex < lsIndex: print(input_string[stIndex:lsIndex])
    else: print(f'{stIndex}:{lsIndex}')
    if match:
        return match.group(1)
    else:
        return None


def save_base64_to_file(base64_content, output_file):
    with open(output_file, 'w', encoding='utf-8') as file:
        file.write(base64_content)

start_marker = "---BEGIN MAZE KEY---"
end_marker = "---END MAZE KEY---"
def extract_key(input_string):
    return extract_between_markers(input_string, start_marker, end_marker)


def decrypt_maze_key(filename: str):
    if not filename: raise ValueError(f'filename Required for decryption')
    RSA_KEY_SIZE = 256
    RSA_PRIV_KEY_BLOB_SIZE = 1172
    CHACHA_ROUNDS = 8
    SENTINEL_SIZE = 16

    with io.open(filename, 'rb') as f:
        data = base64.b64decode(f.read())

    for key_file_index in range(1, 40):
        key_file_path = f'Keys/private_master{key_file_index}.bin'

        try:
            with io.open(key_file_path, 'rb') as key_file:
                master_key_blob = key_file.read()

            master_priv_key = rsa_construct_blob(master_key_blob)

            pos = RSA_PRIV_KEY_BLOB_SIZE
            enc_priv_key_blob = data[:pos]
            enc_chacha_key = data[pos: pos + RSA_KEY_SIZE]
            pos += RSA_KEY_SIZE
            enc_chacha_nonce = data[pos: pos + RSA_KEY_SIZE]
            pos += RSA_KEY_SIZE

            cipher = PKCS1_v1_5.new(master_priv_key)
            sentinel = os.urandom(SENTINEL_SIZE)
            chacha_key = cipher.decrypt(enc_chacha_key[::-1], sentinel)
            if chacha_key == sentinel:
                print(f'Failed to decrypt ChaCha20 key for key file {key_file_index}')
                continue

            sentinel = os.urandom(SENTINEL_SIZE)
            chacha_nonce = cipher.decrypt(enc_chacha_nonce[::-1], sentinel)
            if chacha_nonce == sentinel:
                print(f'Failed to decrypt ChaCha20 nonce for key file {key_file_index}')
                continue

            cipher = chacha.ChaCha(chacha_key, chacha_nonce, 0, CHACHA_ROUNDS)
            priv_key_blob = cipher.decrypt(enc_priv_key_blob)
            priv_key = rsa_construct_blob(priv_key_blob)

            print(f'ChaCha20 key size: {len(chacha_key)}')
            print(f'ChaCha20 nonce size: {len(chacha_nonce)}')
            print(f'Private RSA key size: {priv_key.size_in_bits()}')

            with io.open('private.bin', 'wb') as f:
                f.write(priv_key_blob)

            return priv_key

        except FileNotFoundError:
            print(f'Key file not found: {key_file_path}')
            continue

    return None
