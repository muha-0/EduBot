from ..Database import DBClient
from ..LLM import LLM


class Controller:
    llm = LLM()
    DB_client = DBClient()

    @staticmethod
    def generate(message):
        Controller.llm.generate(message)
