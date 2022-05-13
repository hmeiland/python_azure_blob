#!/usr/bin/env python3
import asyncio
import threading
import random
from string import ascii_lowercase

#from azure.storage.blob.aio import BlobClient, ContainerClient
from azure.storage.blob import BlobClient, ContainerClient

print("prepping random data")
from random import choice
data = ''.join([choice(ascii_lowercase) for _ in range(8*1024*1024)])
print("random data ready...")


#async def upload_blob(idx: int, threshold: int = 6) -> int:
def upload_blob(idx: int, threshold: int = 6) -> int:
    print(f"Initiated upload_blob({idx}).")
    # Upload content to block blob
    sas_url = f"https://azhopwcp6hesz.blob.core.windows.net/async-upload/blob_{idx}?<sas_key>"
    #async with BlobClient.from_blob_url(sas_url) as blob_client:
    with BlobClient.from_blob_url(sas_url) as blob_client:
      blob_client.upload_blob(data, blob_type="BlockBlob")
      #await blob_client.upload_blob(data, blob_type="BlockBlob")
    print(f"---> Finished: upload_blob({idx})")
    return 

async def asynio_main():
    res = await asyncio.gather(*(upload_blob(i, 10 - i - 1) for i in range(1024)))
    return res

def thread_main():
    threads = list()
    for index in range(10240):
        print(f"Main    : create and start thread {index}.")
        x = threading.Thread(target=upload_blob, args=(index,))
        threads.append(x)
        x.start()

    for index, thread in enumerate(threads):
        print(f"Main    : before joining thread {index}.")
        thread.join()
        print(f"Main    : thread {index} done")


if __name__ == "__main__":
    import time
    s = time.perf_counter()
    #asyncio.run(asyncio_main())
    thread_main()
    print(f"all done now...")
    elapsed = time.perf_counter() - s
    print(f"{__file__} executed in {elapsed:0.2f} seconds.")

