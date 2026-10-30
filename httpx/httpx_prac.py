import httpx

"""
httpx library used to call the external api, main advantage compared to requests library is
it can call Ascynchronously

methods:

response.status_code
response.headers
response.text
response.content
response.json()
response.url
response.request
"""

resposne = httpx.get("https://jsonplaceholder.typicode.com/posts/1")

print(resposne.status_code)
print(resposne.text)

print("Completed the request")

"""
The above code is a synchronous code which will block/freeze the python thread, 
for this we use AsyncClient
"""
