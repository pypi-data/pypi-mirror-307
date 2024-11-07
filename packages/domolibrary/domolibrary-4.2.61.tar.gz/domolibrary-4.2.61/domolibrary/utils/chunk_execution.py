# AUTOGENERATED! DO NOT EDIT! File to edit: ../../nbs/utils/chunk_execution.ipynb.

# %% auto 0
__all__ = ['run_with_retry', 'gather_with_concurrency', 'run_sequence', 'chunk_list']

# %% ../../nbs/utils/chunk_execution.ipynb 2
from typing import Any, Awaitable,Callable, Tuple
import asyncio
import functools
import httpx

import domolibrary.client.DomoError as dmde

# %% ../../nbs/utils/chunk_execution.ipynb 3
def run_with_retry(max_retry : int = 1, 
                   errors_to_retry_tp : Tuple = None):
    
    errors_to_retry_tp = errors_to_retry_tp or ()

    """runs a function with an automatic retry if it throws any sort of Exception"""
    def actual_decorator(run_fn: Callable):
        
        @functools.wraps(run_fn)
        async def wrapper( *args, **kwargs ) :

            retry = 0 
            
            while retry <= max_retry:
                try:
                    return await run_fn( *args, **kwargs)
                
                except httpx.ConnectTimeout:
                    await asyncio.sleep(2)
                    retry +=1

                except Exception as e:
                    retry +=1

                    if isinstance(e, dmde.DomoError) and (errors_to_retry_tp and not any(( e for err in errors_to_retry_tp if isinstance(e , err)))):
                        raise e from e

                    if retry > max_retry:
                        raise e from e
                    
                    print(f"retry decorator attempt - {retry}, {e}")
                        
        return wrapper

    return actual_decorator

# %% ../../nbs/utils/chunk_execution.ipynb 5
async def gather_with_concurrency(
    *coros,  # list of coroutines to await
    n=60,  # number of open coroutines
):
    """limits the number of open coroutines at a time."""

    semaphore = asyncio.Semaphore(n)

    async def sem_coro(coro):
        async with semaphore:
            return await coro

    return await asyncio.gather(*(sem_coro(c) for c in coros))

# %% ../../nbs/utils/chunk_execution.ipynb 8
async def run_sequence(
    *functions: Awaitable[Any],  # comma separated list of functions
) -> None:  # no explicit return
    """executes a sequence of functions"""

    return [await function for function in functions]

# %% ../../nbs/utils/chunk_execution.ipynb 11
def chunk_list(
    obj_ls: list[any],  # list of entities to split into n chunks
    chunk_size: int,  # entities per sub list
) -> list[list[dict]]:  # returns a list of chunk_size lists of objects

    return [
        obj_ls[i * chunk_size : (i + 1) * chunk_size]
        for i in range((len(obj_ls) + chunk_size - 1) // chunk_size)
    ]
