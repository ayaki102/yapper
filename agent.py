import time
import random
import requests
import subprocess

SERVER = "http://0.0.0.0:42069"

while True:
    random_int = random.randint(1,40)
    r = requests.get(f"{SERVER}/get_tts").json()
    if r["text"]:
        subprocess.run([
             "espeak-ng", "-v", "pl", "-s",  "100" ,"-p", "1", "-g", "10", r["text"]
        ])

    print("spie przez: ", random_int)
    time.sleep(random_int)

