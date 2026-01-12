"""Flask API client for making LLM requests."""

import httpx
import time
from typing import List, Dict, Any, Optional


async def query_model(
    model_config: Dict[str, str],
    messages: List[Dict[str, str]]
) -> Optional[Dict[str, Any]]:
    """
    Query a single model via Flask API.

    Args:
        model_config: Dict with 'model_name' and 'flask_url' keys
        messages: List of message dicts with 'role' and 'content'

    Returns:
        Response dict with 'content' and 'duration_seconds', or None if failed
    """
    
    flask_url = model_config['flask_url']
    chat_endpoint = f"{flask_url}/chat"
    
    headers = {
        "Content-Type": "application/json",
    }

    payload = {
        "messages": messages,
    }

    start_time = time.time()
    
    try:
        # Set timeout to None to let Flask API handle its own timeout
        async with httpx.AsyncClient(timeout=None) as client:
            response = await client.post(
                chat_endpoint,
                headers=headers,
                json=payload
            )
            end_time = time.time()
            duration = end_time - start_time
            
            response.raise_for_status()

            data = response.json()
            
            content = data['message']['content']

            return {
                'content': content,
                'duration_seconds': round(duration, 2)
            }

    except Exception as e:
        end_time = time.time()
        duration = end_time - start_time
        print(f"Error querying model {model_config.get('model_name', 'unknown')} at {flask_url}: {e}")
        print(f"Request took {duration:.2f}s before failing")
        import traceback
        traceback.print_exc()
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


async def check_model_health(flask_url: str) -> bool:
    """
    Check if a Flask API endpoint is healthy.

    Args:
        flask_url: Base URL of the Flask API

    Returns:
        True if healthy, False otherwise
    """
    health_endpoint = f"{flask_url}/health"
    
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.get(health_endpoint)
            return response.status_code == 200
    except Exception:
        return False


async def check_all_models_health(model_configs: List[Dict[str, str]]) -> Dict[str, bool]:
    """
    Check health of all model endpoints.

    Args:
        model_configs: List of model config dicts with 'model_name' and 'flask_url'

    Returns:
        Dict mapping model name to health status (True/False)
    """
    import asyncio
    
    # Create tasks for all health checks
    tasks = [check_model_health(config['flask_url']) for config in model_configs]
    
    # Wait for all to complete
    health_statuses = await asyncio.gather(*tasks)
    
    # Map model names to their health status
    return {config['model_name']: status for config, status in zip(model_configs, health_statuses)}
