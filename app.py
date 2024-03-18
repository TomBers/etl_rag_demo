import os
from typing import List

from langchain.vectorstores.pinecone import Pinecone as PineconeVectorStore
from langchain.chains import ConversationalRetrievalChain
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain.memory import ChatMessageHistory, ConversationBufferMemory
from langchain.prompts import SystemMessagePromptTemplate, HumanMessagePromptTemplate, ChatPromptTemplate
from langchain.docstore.document import Document
from pinecone import Pinecone
import chainlit as cl

pc = Pinecone(
        api_key=os.environ.get("PINECONE_API_KEY")
    )

index_name = "energytechnologylist"

# Optional
namespace = None

EMBEDDING_MODEL_NAME = "text-embedding-3-small"

embeddings = OpenAIEmbeddings(model=EMBEDDING_MODEL_NAME)

# welcome_message = "Looking to purchase energy efficient products or get impartial advice on making energy savings?  Ask anything about the UK Energy Technology List (ETL), one of the world\\'s largest databases of energy-saving technology. Includes sustainability information on 8,000 tested and assessed energy efficient products, including boilers, electric motors, air conditioning and refrigeration equipment."
welcome_message = """Looking to purchase energy efficient products or get impartial advice on making energy savings?  
Talk directly to the [UK Energy Technology List (ETL)](https://etl.energysecurity.gov.uk), one of the world's largest databases of energy-saving technology. Includes sustainability information on 8,000 tested and assessed energy efficient products, including boilers, electric motors, air conditioning and refrigeration equipment.  
**Sample Question (paste it below)**:
We have limited space but also need plenty of refrigerated storage for food and beverages. What do you have and how do they compare for energy cost?"""

@cl.on_chat_start
async def start():
    await cl.Message(content=welcome_message).send()
    
    docsearch = PineconeVectorStore.from_existing_index(
        index_name=index_name, embedding=embeddings, namespace=namespace
    )

    message_history = ChatMessageHistory()

    memory = ConversationBufferMemory(
        memory_key="chat_history",
        output_key="answer",
        chat_memory=message_history,
        return_messages=True,
    )
    
        
    general_system_template = (r""" 
        *** REED EDIT HERE ***.
        ----
        {context}
        ----
        """)
    
    general_user_template = "Question:```{question}```"
    messages = [
                SystemMessagePromptTemplate.from_template(general_system_template),
                HumanMessagePromptTemplate.from_template(general_user_template)
    ]
    qa_prompt = ChatPromptTemplate.from_messages( messages )

    chain = ConversationalRetrievalChain.from_llm(
        ChatOpenAI(model_name="gpt-4-0125-preview", temperature=0, streaming=True),
        chain_type="stuff",
        retriever=docsearch.as_retriever(),
        combine_docs_chain_kwargs={"prompt": qa_prompt},
        memory=memory,
        return_source_documents=True,
    )
    cl.user_session.set("chain", chain)


@cl.on_message
async def main(message: cl.Message):
    msg = cl.Message(content="")
    await msg.send()
    
    chain = cl.user_session.get("chain")  # type: ConversationalRetrievalChain

    cb = cl.AsyncLangchainCallbackHandler()

    res = await chain.ainvoke(message.content, callbacks=[cb])
    answer = res["answer"]
    source_documents = res["source_documents"]  # type: List[Document]

    text_elements = []  # type: List[cl.Text]

    if source_documents:
        for source_idx, source_doc in enumerate(source_documents):
            source_name = f"source_{source_idx}"
            # Create the text element referenced in the message
            text_elements.append(
                cl.Text(content=source_doc.page_content, name=source_name)
            )
        source_names = [text_el.name for text_el in text_elements]

        if source_names:
            answer += f"\nSources: {', '.join(source_names)}"
        else:
            answer += "\nNo sources found"

    await cl.Message(content=answer, elements=text_elements).send()