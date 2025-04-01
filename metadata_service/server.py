from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict

app = FastAPI()

class FileMetadata(BaseModel):
    shards: Dict[str, list]
    replica_count: int = 3

metadata_db = {}

@app.post("/metadata/{file_id}")
async def update_metadata(file_id: str, metadata: FileMetadata):
    metadata_db[file_id] = metadata.dict()
    return {"status": "success"}

@app.get("/metadata/{file_id}")
async def get_metadata(file_id: str):
    if file_id not in metadata_db:
        raise HTTPException(status_code=404, detail="File not found")
    return metadata_db[file_id]