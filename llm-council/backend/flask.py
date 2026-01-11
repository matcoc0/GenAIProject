"""Flask API client for making LLM requests."""

import httpx
from typing import List, Dict, Any, Optional


async def query_model(
    model_config: Dict[str, str],
    messages: List[Dict[str, str]],
    timeout: float = 120.0
) -> Optional[Dict[str, Any]]:
    """
    Query a single model via Flask API.

    Args:
        model_config: Dict with 'model_name' and 'flask_url' keys
        messages: List of message dicts with 'role' and 'content'
        timeout: Request timeout in seconds

    Returns:
        Response dict with 'content', or None if failed
    """
    flask_url = model_config['flask_url']
    chat_endpoint = f"{flask_url}/chat"
    
    headers = {
        "Content-Type": "application/json",
    }

    payload = {
        "messages": messages,
    }

    try:
        async with httpx.AsyncClient(timeout=timeout) as client:
            response = await client.post(
                chat_endpoint,
                headers=headers,
                json=payload
            )
            response.raise_for_status()

            data = response.json()
            
            content = data['message']['content']

            return {
                'content': content
            }

    except Exception as e:
        print(f"Error querying model at {flask_url}: {e}")
        return None


async def query_models_parallel(
    model_configs: List[Dict[str, str]],
    messages: List[Dict[str, str]]
) -> Dict[str, Optional[Dict[str, Any]]]:
    """
    Query multiple models in parallel.

    Args:
        model_configs: List of model config dicts with 'model_name' and 'flask_url'
        messages: List of message dicts to send to each model

    Returns:
        Dict mapping model name to response dict (or None if failed)
    """
    import asyncio

    # Create tasks for all models
    tasks = [query_model(model_config, messages) for model_config in model_configs]

    # Wait for all to complete
    responses = await asyncio.gather(*tasks)

    # Map model names to their responses
    return {model_config['model_name']: response for model_config, response in zip(model_configs, responses)}
