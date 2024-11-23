from model import *
from utils import *


def generate(query: str):
    context = find_match(query)
    convo.send_message(f"Context:\n{context} \n\n{query}")
    res = convo.last.text.rstrip()
    print(res)
    return res if res != "" else "I don't have this information"


if __name__ == "__main__":
    x = input("Enter Prompt: ")
    print(generate(x))
