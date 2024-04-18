import os
import sys
import requests
import time
import threading
import multiprocessing
import asyncio
import aiohttp

from flask import Flask

app = Flask(__name__)

@app.route("/")
def index():
    urls = sys.argv[1:]
    start_time = time.time()

    # Multithreading
    print("Multithreading:")
    threads = []
    for url in urls:
        thread = threading.Thread(target=download_image, args=(url,))
        thread.start()
        threads.append(thread)
    for thread in threads:
        thread.join()

    # Multiprocessing
    print("\nMultiprocessing:")
    processes = []
    for url in urls:
        process = multiprocessing.Process(target=download_image, args=(url,))
        process.start()
        processes.append(process)
    for process in processes:
        process.join()

    # Asynchronous
    print("\nAsynchronous:")
    loop = asyncio.get_event_loop()
    tasks = [download_image_async(url) for url in urls]
    loop.run_until_complete(asyncio.gather(*tasks))

    total_time = time.time() - start_time
    print(f"\nTotal execution time: {total_time:.2f} seconds")

    return "Images downloaded successfully!"

def download_image(url):
    filename = url.split('/')[-1]
    response = requests.get(url)
    with open(filename, 'wb') as f:
        f.write(response.content)
    print(f"Downloaded {filename}")

async def download_image_async(url):
    filename = url.split('/')[-1]
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            with open(filename, 'wb') as f:
                while True:
                    chunk = await response.content.read(1024)
                    if not chunk:
                        break
                    f.write(chunk)
    print(f"Downloaded {filename}")

if __name__ == "__main__":
    app.run(debug=True)
