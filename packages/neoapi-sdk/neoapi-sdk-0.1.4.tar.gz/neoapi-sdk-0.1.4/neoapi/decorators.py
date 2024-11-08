import asyncio
import functools
import logging
import time
from typing import Any, Callable, Dict, Optional, Union

from .client_async import NeoApiClientAsync
from .client_sync import NeoApiClientSync
from .models import LLMOutput

logger = logging.getLogger(__name__)


def track_llm_output(
    client: Any,
    project: str = "default_project",
    group: str = "default_group",
    analysis_slug: Optional[str] = None,
    need_analysis_response: bool = False,
    format_json_output: bool = False,
    metadata: Optional[Dict[str, Any]] = None,
    save_text: bool = True,
    prompt: Optional[Union[str, Callable[[str], str]]] = None,
) -> Callable:
    """
    Decorator to automatically track LLM outputs.

    Args:
        client (NeoApiClientAsync or NeoApiClientSync): The Neo API client instance.
        project (str): Project name. Defaults to "default_project".
        group (str): Group name. Defaults to "default_group".
        analysis_slug (Optional[str]): Analysis slug.
        need_analysis_response (bool): Whether an analysis response is needed.
        format_json_output (bool): Whether to format the output as JSON.
        metadata (Optional[Dict[str, Any]]): Additional metadata to include in the output.
        save_text (bool): Whether to save the text.
        prompt (Optional[Union[str, Callable[[str], str]]]): Prompt to include in the output.

    Returns:
        Callable: The decorated function.
    """

    def decorator(func: Callable) -> Callable:
        if asyncio.iscoroutinefunction(func):

            @functools.wraps(func)
            async def async_wrapper(*args: Any, **kwargs: Any) -> Any:
                try:
                    result = await func(*args, **kwargs)
                except Exception as e:
                    logger.exception(f"Error in function '{func.__name__}': {e}")
                    raise

                prompt_value = None
                if prompt is not None:
                    if callable(prompt):
                        # If prompt is a function, call it with the first argument
                        if args:
                            prompt_value = prompt(args[0])
                    else:
                        # If prompt is a string, use it directly
                        prompt_value = prompt

                # Convert result to string if it's not already
                text_result = str(result) if not isinstance(result, str) else result

                llm_output = LLMOutput(
                    text=text_result,
                    prompt=prompt_value,
                    project=project,
                    group=group,
                    analysis_slug=analysis_slug,
                    need_analysis_response=need_analysis_response,
                    format_json_output=format_json_output,
                    metadata=metadata,
                    save_text=save_text,
                    timestamp=time.time(),
                )

                if isinstance(client, NeoApiClientAsync):
                    try:
                        await client.track(llm_output)
                    except Exception as e:
                        logger.exception(f"Failed to track LLM output: {e}")
                elif isinstance(client, NeoApiClientSync):
                    try:
                        client.track(llm_output)
                    except Exception as e:
                        logger.exception(f"Failed to track LLM output: {e}")
                else:
                    logger.error("Unsupported client type provided to decorator.")

                return result

            return async_wrapper
        else:

            @functools.wraps(func)
            def sync_wrapper(*args: Any, **kwargs: Any) -> Any:
                try:
                    result = func(*args, **kwargs)
                except Exception as e:
                    logger.exception(f"Error in function '{func.__name__}': {e}")
                    raise

                prompt_value = None
                if prompt is not None:
                    if callable(prompt):
                        # If prompt is a function, call it with the first argument
                        if args:
                            prompt_value = prompt(args[0])
                    else:
                        # If prompt is a string, use it directly
                        prompt_value = prompt

                # Convert result to string if it's not already
                text_result = str(result) if not isinstance(result, str) else result

                llm_output = LLMOutput(
                    text=text_result,
                    prompt=prompt_value,
                    project=project,
                    group=group,
                    analysis_slug=analysis_slug,
                    need_analysis_response=need_analysis_response,
                    format_json_output=format_json_output,
                    metadata=metadata,
                    save_text=save_text,
                    timestamp=time.time(),
                )

                if isinstance(client, NeoApiClientSync):
                    try:
                        client.track(llm_output)
                    except Exception as e:
                        logger.exception(f"Failed to track LLM output: {e}")
                else:
                    logger.error(
                        "For synchronous functions, please provide a NeoApiClientSync instance."
                    )

                return result

            return sync_wrapper

    return decorator
