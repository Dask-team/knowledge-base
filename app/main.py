from typing import List, Optional

from elasticsearch import Elasticsearch
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from app.keyword import extract_keywords

app = FastAPI(title="DasKnB API")
es = Elasticsearch("http://localhost:9200/")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(Exception)
async def error_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content={"message": f"{exc}"}
    )


@app.get("/")
def collections():
    """Get all collections(indexes) in the Elasticsearch server"""
    res = es.cat.indices(h="index", format="json")
    return [index["index"] for index in res]


@app.post("/{collection_name}/_create")
def create_collection(collection_name: str):
    """Create a new collection"""
    query = {
        "settings": {
            "number_of_shards": 1,
            "number_of_replicas": 1,
            "analysis": {
                "analyzer": {
                    "korean_analyzer": {
                        "type": "custom",
                        "tokenizer": "nori_tokenizer"
                    }
                }
            }
        },
        "mappings": {
            "properties": {
                "uuid": {
                    "type": "keyword"
                },
                "title": {
                    "type": "text",
                    "analyzer": "korean_analyzer"
                },
                "body": {
                    "type": "text",
                    "analyzer": "korean_analyzer"
                },
                "tags": {
                    "type": "keyword"
                },
                "created_at": {
                    "type": "date",
                    "format": "strict_date_optional_time||epoch_millis"
                },
                "updated_at": {
                    "type": "date",
                    "format": "strict_date_optional_time||epoch_millis"
                }
            }
        }
    }

    res = es.indices.create(index=collection_name, body=query)
    return res


@app.get("/{collection_name}")
def get_collection(collection_name: str):
    """Get all documents in a collection"""
    res = es.search(index=collection_name, body={"query": {"match_all": {}}})
    return res["hits"]["hits"]


@app.get("/{collection_name}/{document_id}")
def get_document(collection_name: str, document_id: str):
    """Get a document by its id"""
    res = es.get(index=collection_name, id=document_id)
    return res["_source"]


class Document(BaseModel):
    title: str
    content: str
    tags: Optional[List[str]] = []




@app.post("/extract-keywords/")
def extract_keywords(query: str):
    """Extract keywords extract_keywords"""
    return extract_keywords(query)


@app.post("/{collection_name}")
def create_document(collection_name: str, document: Document):
    """Create a new document in a collection"""
    res = es.index(index=collection_name, body=document.dict())
    return res


@app.put("/{collection_name}/{document_id}")
def update_document(collection_name: str, document_id: str, document: Document):
    """Update a document by its id"""
    res = es.update(index=collection_name, id=document_id, body={"doc": document.dict()})
    return res


@app.delete("/{collection_name}/{document_id}")
def delete_document(collection_name: str, document_id: str):
    """Delete a document by its id"""
    res = es.delete(index=collection_name, id=document_id)
    return res


@app.get("/{collection_name}/_search")
def search_documents(collection_name: str, query: str):
    """Search documents in a collection"""
    res = es.search(index=collection_name, body={"query": {"match": {"content": query}}})
    return res["hits"]["hits"]


@app.get("/{collection_name}/tags/{tag}")
def get_documents_by_tag(collection_name: str, tag: str):
    """Get documents by tag"""
    res = es.search(index=collection_name, body={"query": {"match": {"tags": tag}}})
    return res["hits"]["hits"]


@app.get("/{collection_name}/tags")
def get_tags(collection_name: str):
    """Get all tags in a collection"""
    res = es.search(index=collection_name, body={"aggs": {"tags": {"terms": {"field": "tags"}}}})
    return res["aggregations"]["tags"]["buckets"]
