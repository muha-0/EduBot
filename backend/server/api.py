import time

from dotenv import load_dotenv

load_dotenv()
from multiprocessing import Process, Queue

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()
app.add_middleware(
    CORSMiddleware, allow_origins=["*"], allow_credentials=False, allow_methods=["*"], allow_headers=["*"]
)  # Allow CORS for all origins


class MessageRequestModel(BaseModel):
    message: str


def generate(message, result_queue):
    s = time.time()
    from backend.controller import Controller
    print(time.time() - s)

    Controller.generate(message, result_queue)


@app.post("/generate")
def receive_data(payload: MessageRequestModel):
    result_queue = Queue()

    process = Process(target=generate, args=(payload.message, result_queue))
    process.start()
    process.join()

    return result_queue.get()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("api:app", host="localhost", port=2000)
