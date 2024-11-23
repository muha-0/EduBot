from ..LLM import LLM
from ..database import DBClient


class Controller:
    llm = LLM()
    DB_client = DBClient()

    @staticmethod
    def generate(message):
        return Controller.llm.context_analysis(message)
