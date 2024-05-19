from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams
from qdrant_client.models import PointStruct
from uuid import uuid4
import tensorflow_hub as hub


client = QdrantClient(
    host = "localhost",
    port = 6333
)

module_url = "https://tfhub.dev/google/universal-sentence-encoder/4"
model = hub.load(module_url)

def embed(text: list|str) -> list[float]:
    is_str = isinstance(text, str)
    if is_str:
        text = [text]
    output = model(text).numpy().tolist()
    if is_str:
       output = output[0]
    return output

def create_vector_collection(questions: list, answers: list) -> str:
    
    collection_name = str(uuid4())
    # embed the questions
    embeded_questions = [embed(question) for question in questions]
    # create collection
    client.create_collection(
        collection_name = collection_name,
        vectors_config = VectorParams(size=512, distance=Distance.COSINE)
    )

    client.upsert(
        collection_name= collection_name,
        points = [
            PointStruct(
                id = str(uuid4()),
                vector=embed_question,
                payload={
                    "question": question,
                    "answer": answer
                }
            )
            for embed_question, question, answer in zip(embeded_questions, questions, answers)
        ]
    )

    return collection_name
"""
http://chatbot-generator.com/get_answer
{
    "id": collection_name,
    "question": "my question?"
}
return {
    "answer" : get_answer(payload["question"])
}
"""
def get_answer(collection_name: str, question: str, threshold: float = 0.25) -> str:
    question_embed = embed(question)
    results = client.search(
        collection_name = collection_name,
        query_vector = question_embed,
        limit = 1
    )
    
    if not bool(results) or results[0].score < threshold:
        return "Sorry I don't know how to answer your question"
    else:
        return results[0].payload['answer']
