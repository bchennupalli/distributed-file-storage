import os
import hashlib

def shard_file(file_path: str, chunk_size: int = 64 * 1024 * 1024) -> list[str]:
    shard_ids = []
    with open(file_path, "rb") as f:
        chunk_number = 0
        while (chunk := f.read(chunk_size)):
            shard_id = hashlib.sha256(chunk).hexdigest()
            shard_ids.append(shard_id)
            with open(f"shards/{shard_id}", "wb") as shard_file:
                shard_file.write(chunk)
            chunk_number += 1
    return shard_ids