#!/usr/bin/env python3
import asyncio
import random
from string import ascii_lowercase

from azure.storage.blob.aio import BlobClient, ContainerClient

print("prepping random data")
from random import choice
data = ''.join([choice(ascii_lowercase) for _ in range(8*1024*1024)])
print("random data ready...")


async def upload_blob(idx: int, threshold: int = 6) -> int:
    print(f"Initiated upload_blob({idx}).")
    # Upload content to block blob
    sas_url = f"https://azhopwcp6hesz.blob.core.windows.net/async-upload/blob_{idx}?sp=racwdli&st=2022-05-13T10:33:17Z&se=2022-05-31T18:33:17Z&spr=https&sv=2020-08-04&sr=c&sig=q0sw636ZieYPYXcxthmJpApmm5mFgUE%2FjxXMXjii%2B%2FI%3D"
    async with BlobClient.from_blob_url(sas_url) as blob_client:
      await blob_client.upload_blob(data, blob_type="BlockBlob")
    print(f"---> Finished: upload_blob({idx})")
    return 

async def main():
    res = await asyncio.gather(*(upload_blob(i, 10 - i - 1) for i in range(1024)))
    return res

if __name__ == "__main__":
    import time
    s = time.perf_counter()
    asyncio.run(main())
    print(f"all done now...")
    elapsed = time.perf_counter() - s
    print(f"{__file__} executed in {elapsed:0.2f} seconds.")

