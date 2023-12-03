import io
import os
import shutil
import sqlite3

from django.http import FileResponse
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.decorators import api_view

from decrypt import *


@api_view(['GET'])
def getShaDetails(request: Request):
    if 'sha' not in request.query_params:
        return Response('please provide sha query parameter to get details')
    sha = request.query_params['sha']
    conn = sqlite3.connect('malware.db')
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM malware_hashes WHERE field2 = ?", (sha,))

    results = cursor.fetchall()

    if results:
        data = {
            'found': True,
            'first_seen_utc': results[0][0],
            'sha256_hash': results[0][1],
            'md5_hash': results[0][2],
            'sha1_hash': results[0][3],
            'reporter': results[0][4],
            'file_name': results[0][5],
            'file_type_guess': results[0][6],
            'mime_type': results[0][7],
            'signature': results[0][8],
            'clamav': results[0][9],
            'vtpercent': results[0][10],
            'imphash': results[0][11],
            'ssdeep': results[0][12],
            'tlsh': results[0][13],
        }
        return Response(data)

    data = {
        'found': False
    }

    return Response(data)


def error(err):
    return Response({"error": str(err)})


@api_view(['GET', 'POST'])
def decryptFile(request: Request):
    try:
        if 'ransom_note' not in request.FILES:
            return error('please provide ransom_note file')
        if 'file_to_decrypt' not in request.FILES:
            return error('please provide file_to_decrypt')

        tmpFileToDecrypt = 'TMP_FileToDecrypt.txt'
        '''saving TMP_FileToDecrypt from api'''
        with open(tmpFileToDecrypt, "wb+") as destination:
            for chunk in request.FILES["file_to_decrypt"].chunks():
                destination.write(chunk)

        tmpRansomNote = 'TMP_RansomNote.txt'
        '''saving TMP_RansomNote from api'''
        with open(tmpRansomNote, "wb+") as destination:
            for chunk in request.FILES["ransom_note"].chunks():
                destination.write(chunk)
        '''Bloc 1'''
        '''Extraction of Private Key form RansomNote and store to decoded_text'''

        try:
            with open(tmpRansomNote, 'r', errors='replace', encoding='utf-16-le') as file:
                input_text = file.read()
        except FileNotFoundError:
            return error(f"File not found: {tmpRansomNote}")

        encoded_string = extract_key(input_text)

        if not encoded_string:
            return error("Markers not found or order is incorrect.")

        print("Encoded String:", encoded_string)
        output_file = "decoded_text.txt"
        save_base64_to_file(encoded_string, output_file)
        print(f"Decoded text saved to {output_file}")

        '''from extracted ransomNote generating .bin file with the help of private master key and store to 
        private.bin'''
        '''Bloc 2'''
        private_key = decrypt_maze_key(output_file)
        if not private_key:
            return error('Failed to decrypt with all key files')
        '''decrypting the files uploaded with the help of private.bin above created'''
        '''Bloc 3'''
        print('Decrypted Maze Key')
        '''Read RSA private key BLOB'''
        with io.open(PrivateBinPath, 'rb') as f:
            priv_key_blob = f.read()

        '''Get RSA private key from BLOB'''
        priv_key = rsa_construct_blob(priv_key_blob)
        if (priv_key is None) or not priv_key.has_private():
            return error('Error: Invalid RSA private key BLOB')
        print('RSA private generated from BLOB')

        '''Copy file'''
        new_filename = tmpFileToDecrypt + '.dec'
        shutil.copy(tmpFileToDecrypt, new_filename)

        '''Decrypt file'''
        if not decrypt_file(new_filename, priv_key):
            os.remove(new_filename)
            return error('Error: Failed to decrypt file')

        print('File decrypted successfully:', new_filename)

        file = open(new_filename, 'rb')
        return FileResponse(file)


    except Exception as e:
        return Response({
            "error": str(e)
        })
