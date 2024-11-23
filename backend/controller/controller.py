from ..LLM import LLM
from ..database import DBClient


class Controller:
    __llm = LLM()
    __DB_client = DBClient()

    @staticmethod
    def generate(message):
        return Controller.__llm.context_analysis(message)


if __name__ == "__main__":
    x = Controller()
