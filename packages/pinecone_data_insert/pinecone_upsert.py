import os
from pinecone import Pinecone
from openai import OpenAI
import time

import etl_extract

INDEX_NAME = "etl"
EMBEDDING_MODEL_NAME = "text-embedding-3-small"

client = OpenAI()

pc = Pinecone(
    api_key=os.environ.get("PINECONE_API_KEY")
)

index = pc.Index(INDEX_NAME)

def run():
    for doc in range(1, 40):
        time.sleep(2)
        products = etl_extract.extract_products(doc)
        for product in products:
            product = etl_extract.process_product(product)
            save_to_index(product)

def save_to_index(product):
    id = product["id"]
    text = product["text"]
    
    ids = [id]
    res = client.embeddings.create(input=text, model=EMBEDDING_MODEL_NAME)
    embeds = [record.embedding for record in res.data]
    meta = [{"text": text}]
    # The actual inset statement
    to_upsert = zip(ids, embeds, meta)
    index.upsert(vectors=list(to_upsert))
    print(f"Upserted {id}")
    
run()