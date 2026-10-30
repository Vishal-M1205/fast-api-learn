"""
When a request fails for timeout, or service unavilable 503, 5xx errors
too many request 429
and other httpx errors like
Timeout , read ,connecterror
we can use retry

the retry mechanism are
exponential backoff

delay = min(base * (2**attempt),16)
await asyncio.sleep(delay)
so at every attempt different delay seconds are used
so that the other retries wont occur at the same time and crash the server

there is another concept jitter - to avoid the thundering herd problem

delay += random.uniform(0,1)

the request will be differ in ms , so every requet wont reach the server at the same time


"""
