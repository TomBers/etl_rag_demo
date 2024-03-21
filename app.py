import os
from typing import List

from langchain.vectorstores.pinecone import Pinecone
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableParallel, RunnablePassthrough
from langchain_openai import ChatOpenAI, OpenAIEmbeddings

from langchain.prompts import  ChatPromptTemplate
from langchain.docstore.document import Document

import chainlit as cl


INDEX_NAME = "etl"
EMBEDDING_MODEL_NAME = "text-embedding-3-small"


# welcome_message = "Looking to purchase energy efficient products or get impartial advice on making energy savings?  Ask anything about the UK Energy Technology List (ETL), one of the world\\'s largest databases of energy-saving technology. Includes sustainability information on 8,000 tested and assessed energy efficient products, including boilers, electric motors, air conditioning and refrigeration equipment."
welcome_message = """Looking to purchase energy efficient products or get impartial advice on making energy savings?  
Talk directly to the [UK Energy Technology List (ETL)](https://etl.energysecurity.gov.uk), one of the world's largest databases of energy-saving technology. Includes sustainability information on 8,000 tested and assessed energy efficient products, including boilers, electric motors, air conditioning and refrigeration equipment.  
**Sample Question (paste it below)**:
We have limited space but also need plenty of refrigerated storage for food and beverages. What do you have and how do they compare for energy cost?"""

@cl.on_chat_start
async def start():
    await cl.Message(content=welcome_message).send()
    
    vectorstore = Pinecone.from_existing_index(
    index_name=INDEX_NAME,
    embedding=OpenAIEmbeddings(model=EMBEDDING_MODEL_NAME),
    namespace=None
    )
    retriever = vectorstore.as_retriever()

    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are an expert on the energy efficiency of products to increase the efficiency of buildings, you have a store of effieienct products the user would like to know more about to help make purchasing decisions."),
        ("system", "Answer the question based only on the following context: {context}"),
        ("user", "Question: {question}")
    ])


    model = ChatOpenAI(model="gpt-4-0125-preview")
    output_parser = StrOutputParser()

    setup_and_retrieval = RunnableParallel(
        {"context": retriever, "question": RunnablePassthrough()}
    )
    chain = setup_and_retrieval | prompt | model | output_parser
    cl.user_session.set("chain", chain)


@cl.on_message
async def main(message: cl.Message):
    msg = cl.Message(content="")
    await msg.send()
    
    chain = cl.user_session.get("chain")
    for chunk in chain.stream(message.content):  
        await msg.stream_token(chunk)

    await cl.Message(content="🤖🤖🤖").send()