import asyncio
import httpx


async def get_post():
    async with httpx.AsyncClient() as client:
        response = await client.get("https://jsonplaceholder.typicode.com/posts/1")

        print(response.json())


"""
For a post httpx request we need to send the header, body, query param
the below code is the example of that 
"""


async def post_example():
    async with httpx.AsyncClient() as client:
        try:
            headers = {"Athouriztion": "Bearer token"}
            response = await client.post(
                "https://api.example.com/students",
                params={"id": 1, "age": 20},  #! One way to send the query params
                headers=headers,  #! for sending headers,
                json={"name": "Vishal", "age": 20},  #! json - represent the json body
                auth=("username", "password"),
                #! the auth will merge the two param convert it into base64 , and attach it into header as auth token
            )

            response.raise_for_status()

            print(response.is_success)
            print(response.is_error)
            #! lot of attribute are like the above one
        except httpx.TimeoutException:
            raise
        except httpx.HTTPStatusError as error:
            print(error.response.status_code)


"""
 raise_for_status() - when error code 4xx or 5xx comes it raise HTTPStatusError
"""


""""
async with httpx.AsyncClient(headers = {....}) as client:

header can be configured in the client to avoid code repetition, but the 
request level header can merge with the client level , 
iif the same header is given in both the level , request will ovveride the client  

"""

"""
By default the connection pool is created in the AsyncClient , but we can configure using the httpx.Limits()

params:
max_connection
max_keepalive_connections - idle connection which is created first, alive for reuse purpose
keepalive_expiry - idle connection 

request waiting to get connection will raise the pool.timeout error if the pool timeout exceeeds 

"""

"""
Timeout - how long the app is taking to connect the server via httpx 

Connect timeout - how long it is taking to connect the resend server it's a example
Your application
       |
       | Establish connection
       v
    Resend API

eg: httpx.Timeout(connect =  5)

if didn't connect in 5 seconds 
http.ConnectTimeout raises

Read Timeout - after the connection , how long the resend server is taking to sendt the response 

eg: httpx.Timeout(read =  5)

if exceeds raises httpx.ReadTimeout

config - write , error -  WriteTimeout - for uploading file chunk by chunk , time is calculated beteween the chunck sending 

PoolTimeout , pool - if a new conncetion which is exceeded the max_connection , will wait for pool time , if time
exceed PoolTimeout raises

All the above expcetion can be caught in httpx.TimeoutException
"""

asyncio.run(get_post())


"""
The above method inefficient because the httpx client request and created and closed, 
if there are 100 request need to me made we cannot close every single one create a new one 
for this , we yeild the async with context manager and pass the client in the application 
using lifespan
"""
