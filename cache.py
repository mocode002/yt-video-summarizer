import redis
import hashlib

redis_client = redis.Redis(host='localhost', port=6379, db=0)

def generate_summary_cache_key(url: str, model: str, style: str) -> str:
    key_string = f"{url}|{model}|{style}"
    return hashlib.sha256(key_string.encode()).hexdigest()

def generate_transcript_cache_key(url: str) -> str:
    return hashlib.sha256(url.encode()).hexdigest()