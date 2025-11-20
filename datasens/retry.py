"""
Module de retry avec backoff exponentiel pour appels API
Utilisé pour rendre les collecteurs robustes face aux erreurs réseau
"""

import time
import logging
from functools import wraps
from typing import Callable, Type, Tuple

logger = logging.getLogger(__name__)


def retry_with_backoff(
    max_retries: int = 3,
    initial_delay: float = 1.0,
    backoff_factor: float = 2.0,
    exceptions: Tuple[Type[Exception], ...] = (Exception,)
):
    """
    Décorateur pour retry automatique avec backoff exponentiel.
    
    Args:
        max_retries: Nombre maximum de tentatives
        initial_delay: Délai initial en secondes
        backoff_factor: Facteur multiplicatif pour chaque retry
        exceptions: Tuple d'exceptions à catcher
        
    Example:
        @retry_with_backoff(max_retries=3, initial_delay=1.0)
        def call_api():
            response = requests.get("https://api.example.com")
            return response.json()
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            delay = initial_delay
            last_exception = None
            
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    last_exception = e
                    
                    if attempt < max_retries - 1:
                        logger.warning(
                            f"⚠️ {func.__name__} échoué (tentative {attempt + 1}/{max_retries}): {str(e)[:100]}"
                        )
                        logger.info(f"⏳ Retry dans {delay:.1f}s...")
                        time.sleep(delay)
                        delay *= backoff_factor
                    else:
                        logger.error(
                            f"❌ {func.__name__} échoué après {max_retries} tentatives: {str(e)[:100]}"
                        )
            
            raise last_exception
        
        return wrapper
    return decorator


def retry_on_network_error(max_retries: int = 3):
    """
    Décorateur spécialisé pour erreurs réseau (requests, urllib)
    """
    import requests
    from urllib3.exceptions import MaxRetryError, NewConnectionError
    
    network_exceptions = (
        requests.exceptions.RequestException,
        requests.exceptions.ConnectionError,
        requests.exceptions.Timeout,
        MaxRetryError,
        NewConnectionError,
        ConnectionError,
    )
    
    return retry_with_backoff(
        max_retries=max_retries,
        initial_delay=1.0,
        backoff_factor=2.0,
        exceptions=network_exceptions
    )
