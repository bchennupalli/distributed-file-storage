from bisect import bisect
import hashlib

class ConsistentHasher:
    def __init__(self, nodes: list[str], replicas: int = 3):
        self.replicas = replicas
        self.ring = []
        self.node_map = {}
        for node in nodes:
            for i in range(replicas):
                key = self._hash(f"{node}-{i}")
                self.ring.append(key)
                self.node_map[key] = node
        self.ring.sort()

    def get_node(self, shard_id: str) -> str:
        key = self._hash(shard_id)
        idx = bisect(self.ring, key) % len(self.ring)
        return self.node_map[self.ring[idx]]
    
    def _hash(self, key: str) -> int:
        return int(hashlib.md5(key.encode()).hexdigest(), 16)
    
    