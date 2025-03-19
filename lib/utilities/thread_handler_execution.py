import numpy as np
import asyncio
from concurrent.futures import ThreadPoolExecutor


async def thread_handler_execution(arr, max_workers, max_thread_pools, callback):

    chunk_size = len(
        arr) // max_thread_pools if max_thread_pools > 0 else 2

    splitted_array = np.array_split(
        arr, chunk_size) if chunk_size > 0 else [arr]

    semaphore = asyncio.Semaphore(max_workers)

    async def limited_data(chunk):

        async with semaphore:
            return await callback(chunk)

    results = await asyncio.gather(*(
        limited_data(chunk)
        for chunk in splitted_array
    ))

    return [item for sublist in results for item in sublist]
