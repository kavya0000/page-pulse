import os
import time
from dotenv import load_dotenv

load_dotenv()


CACHE_TTL_SECONDS = int(
    os.getenv("CACHE_TTL_SECONDS", "300")
)


class TTLCache:

    def __init__(self):
        self.data = {}

    def __contains__(self, key):
        if key in self.data:
            value, timestamp = self.data[key]

            if time.time() - timestamp < CACHE_TTL_SECONDS:
                return True

            del self.data[key]

        return False


    def __getitem__(self, key):
        value, timestamp = self.data[key]
        return value


    def __setitem__(self, key, value):
        self.data[key] = (
            value,
            time.time()
        )


cache = TTLCache()