from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from Generator import *

app = FastAPI()

# Allow CORS for all origins
app.add_middleware(
    CORSMiddleware, allow_origins=["*"], allow_credentials=False, allow_methods=["*"], allow_headers=["*"]
)


class query(BaseModel):
    msg: str


@app.post("/generate")
def receive_data(body: query):
    return generate(body.msg)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("api_gen:app", host="localhost", port=2000, reload=True)
