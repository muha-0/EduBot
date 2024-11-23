from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from backend.controller import Controller

app = FastAPI()
# Allow CORS for all origins
app.add_middleware(
    CORSMiddleware, allow_origins=["*"], allow_credentials=False, allow_methods=["*"], allow_headers=["*"]
)


class MessageRequestModel(BaseModel):
    message: str


@app.post("/generate")
def receive_data(body: MessageRequestModel):
    return Controller.generate(body.message)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("api:app", host="localhost", port=2000, reload=True)
