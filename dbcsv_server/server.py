from fastapi import FastAPI, HTTPException, Response
from fastapi.responses import JSONResponse
from .db_controller import DBController
from pydantic import BaseModel

app = FastAPI()
db_controller = DBController()


class RequestBody(BaseModel):
    connection_id: str
    query: str = None
    query_id: str = None


@app.get("/connect")
def connect():
    con = db_controller.connect()
    return JSONResponse(status_code=200, content={"connection_id": con.id})


@app.post("/query")
def execute(query_request: RequestBody):
    if not query_request.query:
        raise HTTPException(400, "No query provided")
    query_id = db_controller.execute_query(
        query_request.connection_id, query_request.query
    )
    return JSONResponse(status_code=200, content={"query_id": query_id})


@app.get("/close")
def close(query_request: RequestBody):
    if not query_request.connection_id:
        raise HTTPException(400, "Non exists connection id provided")
    db_controller.disconnect(query_request.connection_id)
    return Response(status_code=200)


@app.post("/fetch")
def fetch(request_body: RequestBody):
    if not request_body.query_id:
        raise HTTPException(400, "Missing query id")
    if not request_body.connection_id:
        raise HTTPException(400, "Non existent connection provided")
    row_result = db_controller.fetch_next(
        request_body.connection_id, request_body.query_id
    )
    return JSONResponse(
        status_code=200,
        content={"data": row_result["data"], "description": row_result["description"]},
    )
