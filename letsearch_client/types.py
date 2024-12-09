from pydantic import BaseModel
from typing import List


class ErrorResponse(BaseModel):
    status: str = "error"
    message: str


class HealthcheckResponse(BaseModel):
    version: str
    status: str


class CollectionInfo(BaseModel):
    name: str
    index_columns: List[str]


class CollectionsResponse(BaseModel):
    collections: List[CollectionInfo]


class SearchResult(BaseModel):
    content: str
    key: int
    score: float


class SearchResponse(BaseModel):
    results: List[SearchResult]
