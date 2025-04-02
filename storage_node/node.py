from flask import Flask, request, send_file
import os

app = Flask(__name__)
port = os.environ.get('PORT', "5001")
STORAGE_DIR = os.path.join(os.getcwd(), f'storage_{port}')

@app.route('/shard/<shard_id>', methods=['PUT'])
def upload_shard(shard_id):
    os.makedirs(STORAGE_DIR, exist_ok=True)
    with open(os.path.join(STORAGE_DIR, shard_id), 'wb') as f:
        f.write(request.data)
    return {"status": "success", "shard_id": shard_id}

@app.route('/shard/<shard_id>', methods=['GET'])
def download_shard(shard_id):
    file_path = os.path.join(STORAGE_DIR, shard_id)
    if not os.path.exists(file_path):
        return {"error": "Shard not found"}, 404
    return send_file(file_path)

