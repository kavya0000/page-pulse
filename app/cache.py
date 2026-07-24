from cachetools import TTLCache

# Cache stores up to 100 URLs for 5 minutes
cache = TTLCache(maxsize=100, ttl=300)