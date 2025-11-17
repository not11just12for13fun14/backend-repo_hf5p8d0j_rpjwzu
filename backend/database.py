from typing import Any, Dict, Optional
import os
from datetime import datetime
from pymongo import MongoClient
from pymongo.collection import Collection
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "mongodb://localhost:27017")
DATABASE_NAME = os.getenv("DATABASE_NAME", "duatix")

_client: Optional[MongoClient] = None
_db = None


def get_db():
    global _client, _db
    if _db is None:
        _client = MongoClient(DATABASE_URL)
        _db = _client[DATABASE_NAME]
    return _db


def get_collection(name: str) -> Collection:
    db = get_db()
    return db[name]


def create_document(collection_name: str, data: Dict[str, Any]) -> Dict[str, Any]:
    col = get_collection(collection_name)
    now = datetime.utcnow()
    payload = {**data, "created_at": now, "updated_at": now}
    result = col.insert_one(payload)
    inserted = col.find_one({"_id": result.inserted_id})
    if inserted:
        inserted["id"] = str(inserted.pop("_id"))
    return inserted or {}


def get_documents(collection_name: str, filter_dict: Dict[str, Any] | None = None, limit: int = 100):
    col = get_collection(collection_name)
    cursor = col.find(filter_dict or {}).limit(limit)
    items = []
    for doc in cursor:
        doc["id"] = str(doc.pop("_id"))
        items.append(doc)
    return items
