from utils.file_sharding import shard_file

# Split the file into 10-byte chunks (for testing)
shard_ids = shard_file("large_file.txt", chunk_size=10)

print("Shard IDs:", shard_ids)
