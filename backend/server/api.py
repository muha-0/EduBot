from dotenv import load_dotenv

load_dotenv()
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

try:
    from backend.controller import Controller
except:
    pass

app = FastAPI()
app.add_middleware(
    CORSMiddleware, allow_origins=["*"], allow_credentials=False, allow_methods=["*"], allow_headers=["*"]
)


class MessageRequestModel(BaseModel):
    message: str
    user_id: str


@app.post("/generate")
def receive_data(payload: MessageRequestModel):
    return Controller.generate(payload.message, payload.user_id)


@app.post("/delete-user")
async def delete_user(payload: Request):
    body = await payload.json()
    Controller.delete_user_model(body["user_id"])

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("api:app", host="localhost", port=2000)
