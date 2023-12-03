import sqlite3
import sys

import requests

url = "http://127.0.0.1:8000/check-sha?format=json&sha=094fd325049b8a9cf6d3e5ef2a6d4cc6a567d7d49c35f8bb8dd9e3c6acf3d78d"



response = requests.request("GET", url)

print(response.text)
print(response.json()['found'])
json = response.json()
my_string = "\n".join(["{}: {}".format(key, value) for key, value in json.items()])
print(my_string)

sys.exit()
# ############## Below Test for DB backend data format
conn = sqlite3.connect('malware.db')
cursor = conn.cursor()
cursor.execute(f"SELECT * FROM malware_hashes")

# results = cursor.fetchall()
# i =0
# if results:
#     for i in results:
#         try:
#             print(';'.join(i))
#             cursor.close()
#             conn.close()
#             sys.exit()
#         except Exception as e:
#             print(e)

sha = '094fd325049b8a9cf6d3e5ef2a6d4cc6a567d7d49c35f8bb8dd9e3c6acf3d78d'
cursor = conn.cursor()
cursor.execute(f"SELECT * FROM malware_hashes WHERE field2 = ?", (sha,))

results = cursor.fetchall()

if results:
    data = {
        'result': sha,
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
    print(data)
    print(results)

cursor.close()
conn.close()
