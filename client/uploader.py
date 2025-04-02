import os
import sys
import requests

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

from utils.file_sharding import shard_file
from utils.hashing import ConsistentHasher

STORAGE_NODES = ["http://localhost:5001", "http://localhost:5002", "http://localhost:5003"]
hasher = ConsistentHasher(STORAGE_NODES)

def upload_file(file_path: str):
    shard_ids = shard_file(file_path, chunk_size=10)
    shard_locations = {}
    
    for idx, shard_id in enumerate(shard_ids):
        replica_nodes = hasher.get_nodes(shard_id, replicas=3)
        shard_path = os.path.join(project_root, "shards", shard_id)  
        successful_nodes = []

        for node in replica_nodes:
            try:
                with open(shard_path, "rb") as f:
                    response = requests.put(
                        f"{node}/shard/{shard_id}",
                        data=f
                    )
                    if response.status_code == 200:
                        print(f"Uploaded {shard_id[:8]}... to {node}")
                        successful_nodes.append(node)
                    else:
                        print(f"Failed to upload {shard_id[:8]}... to {node}. Status: {response.status_code}")

            except Exception as e:
                print(f"Error uploading {shard_id[:8]}... to {node}: {str(e)}")

            if successful_nodes:
                shard_locations[str(idx)] = successful_nodes
            else:
                print(f"All replicas failed for shard {shard_id[:8]}...")
                continue

    metadata = {
        "shards": shard_locations,
        "replica_count": 3
    }
    
    try:
        response = requests.post(
            "http://localhost:8000/metadata/large_file.txt",
            json=metadata
        )
        print(f"Metadata updated: {response.json()}")
    except Exception as e:
        print(f"Failed to update metadata: {str(e)}")

if __name__ == "__main__":
    upload_file("large_file.txt")