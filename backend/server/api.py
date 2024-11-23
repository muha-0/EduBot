from multiprocessing import Process, Queue

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


@app.post("/generate")
def receive_data(body: MessageRequestModel):
    result_queue = Queue()

    process = Process(target=Controller.generate, args=(body.message, result_queue))
    process.start()
    process.join()

    result = result_queue.get()
    return result


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("api:app", host="localhost", port=2000)
