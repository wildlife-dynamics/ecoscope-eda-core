import json

import obstore


async def get_results_json(results_url: str) -> dict:
    """Get the results of the workflow run."""
    result_store = obstore.store.from_url(results_url)
    get_result = await result_store.get_async("result.json")
    result_bytes = await get_result.bytes_async()
    if not result_bytes and not isinstance(result_bytes, bytes):
        raise RuntimeError("Failed to get result json from result store.")
    result_json = json.loads(bytes(result_bytes).decode("utf-8"))
    return result_json
