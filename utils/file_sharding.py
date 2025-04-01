import os
import hashlib

def shard_file(file_path: str, chunk_size: int = 64 * 1024 * 1024) -> list[str]:
    shard_ids = []
    with open(file_path, "rb") as f:
        chunk_number = 0
        