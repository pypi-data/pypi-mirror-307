import asyncio
from reactpy import use_state, use_effect

def use_query(query_key, fetch_function, enabled=True, refetch_interval=None):
    """
    A custom hook to handle asynchronous data fetching, caching, and state management in ReactPy.
    
    Parameters:
    - query_key: Unique key to cache the data.
    - fetch_function: Async function to fetch data.
    - enabled: Whether the query should execute on mount.
    - refetch_interval: Interval to refetch the data, in seconds.
    """
    data, set_data = use_state(None)
    error, set_error = use_state(None)
    is_loading, set_is_loading = use_state(enabled)
    is_fetching, set_is_fetching = use_state(False)

    async def fetch_data():
        if not enabled:
            return
        try:
            set_is_loading(True)
            set_is_fetching(True)
            result = await fetch_function()
            set_data(result)
        except Exception as e:
            set_error(e)
        finally:
            set_is_loading(False)
            set_is_fetching(False)

    use_effect(lambda: asyncio.create_task(fetch_data()), [query_key])

    
    if refetch_interval:
        use_effect(
            lambda: asyncio.create_task(fetch_data()),
            interval=refetch_interval,
            repeat=True
        )

    def refetch():
        asyncio.create_task(fetch_data())

    return {
        "data": data,
        "error": error,
        "is_loading": is_loading,
        "is_fetching": is_fetching,
        "refetch": refetch,
    }
