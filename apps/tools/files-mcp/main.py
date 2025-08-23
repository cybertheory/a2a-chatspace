from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any

app = FastAPI(
    title="Files MCP (Master Control Program)",
    description="A tool for reading and writing artifacts to an object store.",
    version="0.1.0"
)

# --- Pydantic Models for Request/Response ---

class ReadRequest(BaseModel):
    path: str

class ReadResponse(BaseModel):
    path: str
    content_b64: str # Content will be base64 encoded

class WriteRequest(BaseModel):
    path: str
    content_b64: str
    meta: Dict[str, Any]

class WriteResponse(BaseModel):
    path: str
    version: str # e.g., an S3 versionId
    size_bytes: int

class ListRequest(BaseModel):
    prefix: str

class ListResponse(BaseModel):
    prefix: str
    files: List[str]

class DiffRequest(BaseModel):
    path_a: str
    path_b: str

class DiffResponse(BaseModel):
    diff: str # A unified diff format string

# --- API Endpoints ---

@app.get("/health")
async def health_check():
    """Basic health check endpoint."""
    return {"status": "ok"}

@app.post("/read")
async def read_file(request: ReadRequest):
    """(Placeholder) Reads a file from the object store."""
    print(f"Reading path: {request.path}")
    # In a real implementation, this would connect to S3/MinIO
    # and fetch the file bytes, then base64 encode them.
    return ReadResponse(path=request.path, content_b64="c2FtcGxlIGNvbnRlbnQ=") # "sample content"

@app.post("/write")
async def write_file(request: WriteRequest):
    """(Placeholder) Writes a file to the object store."""
    print(f"Writing to path: {request.path} with meta: {request.meta}")
    # In a real implementation, this would decode the content
    # and upload it to S3/MinIO.
    return WriteResponse(path=request.path, version="v1.0.0-placeholder", size_bytes=len(request.content_b64))

@app.post("/list")
async def list_files(request: ListRequest):
    """(Placeholder) Lists files with a given prefix."""
    print(f"Listing files with prefix: {request.prefix}")
    return ListResponse(prefix=request.prefix, files=[f"{request.prefix}/file1.txt", f"{request.prefix}/file2.txt"])

@app.post("/version")
async def version_file(request: ReadRequest):
    """(Placeholder) Gets versions of a file."""
    print(f"Versioning path: {request.path}")
    return {"path": request.path, "versions": ["v1.0.0-placeholder", "v0.9.0-placeholder"]}

@app.post("/diff")
async def diff_files(request: DiffRequest):
    """(Placeholder) Diffs two files."""
    print(f"Diffing {request.path_a} and {request.path_b}")
    diff_text = f"--- {request.path_a}\n+++ {request.path_b}\n@@ -1 +1 @@\n-old content\n+new content"
    return DiffResponse(diff=diff_text)
