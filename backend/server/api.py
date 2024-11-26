from dotenv import load_dotenv

load_dotenv()
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from backend.controller import Controller

app = FastAPI()
app.add_middleware(
    CORSMiddleware, allow_origins=["*"], allow_credentials=False, allow_methods=["*"], allow_headers=["*"]
)  # Allow CORS for all origins


class MessageRequestModel(BaseModel):
    message: str
    user_id: str


@app.post("/generate")
def receive_data(payload: MessageRequestModel):
    return Controller.generate(payload.message, payload.user_id)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("api:app", host="localhost", port=2000)
