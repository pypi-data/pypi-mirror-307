# Reactpy-query
tanstack query like function for reactpy

# How to use?
```python
import httpx

async def fetch_data():
    async with httpx.AsyncClient() as client:
        response = await client.get("https://jsonplaceholder.typicode.com/posts")
        return response.json()

def MyComponent():
    query = use_reactpy_query("posts", fetch_data, enabled=True, refetch_interval=60)

    if query["is_loading"]:
        return "Loading..."

    if query["error"]:
        return f"Error: {query['error']}"

    return query["data"]
```