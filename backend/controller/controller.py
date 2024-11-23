from ..LLM import LLM
from ..database import DBClient


class Controller:
    __llm = LLM()
    __DB_client = DBClient()

    @staticmethod
    def generate(message, result_queue):
        result_queue.put(Controller.__llm.context_analysis(message))


if __name__ == "__main__":
    import time

    s = time.time()
    x = Controller()
    print(time.time() - s)
