import pinecone
from sentence_transformers import SentenceTransformer

model = SentenceTransformer('all-mpnet-base-v2')
index = pinecone.Pinecone(api_key='d735e8ad-5744-4ccf-9c71-6ad3a09cf818')
index = index.Index('eui')


def find_match(input):
    input_em = model.encode(input).tolist()
    result = index.query(vector=input_em, top_k=3, includeMetadata=True)
    return result['matches'][0]['metadata']['text'] + "\n" + result['matches'][1]['metadata']['text'] + \
        result['matches'][2]['metadata']['text']

# def query_refiner(conversation, query):
#
#     response = openai.Completion.create(
#     model="text-davinci-003",
#     prompt=f"Given the following user query and conversation log, formulate a question that would be the most relevant to provide the user with an answer from a knowledge base.\n\nCONVERSATION LOG: \n{conversation}\n\nQuery: {query}\n\nRefined Query:",
#     temperature=0.7,
#     max_tokens=256,
#     top_p=1,
#     frequency_penalty=0,
#     presence_penalty=0
#     )
#     return response['choices'][0]['text']

# def get_conversation_string():
#     return conversation_string
