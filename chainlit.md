# AI Assistant for the **Energy Technology List (ETL)** 

Designed by [**Assistant Engineering**](https://assistant.engineering), this chatbot uses the Chainlit framework to  demonstrate the combination of a custom knowledge source with a Large Language Model (LLM) to tailor the Assistant to a particular topic.

**How It Works**:
We start by calling the ETL's Application Programming Interface (API) to collect their green energy product list. We vectorise this data and store it in a vector database.  

Then we use Retrieval Augmented Generation (RAG) to connect that database to the LLM as a specialised knowledge source. We also provide some custom instructions and tuning prompts to the LLM.

The result is a natural language interface that makes it easy to engage with and inquire about the 8,000 sustainable energy products in the ETL list.  We can do this sort of thing with many, many data sources. 🚀🤖

**About The ETL**:
[The Energy Technology List (ETL)](https://etl.energysecurity.gov.uk) is a UK government initiative backed by the Department for Energy Security and Net Zero. It assists businesses and the public sector in choosing greener energy solutions. Free to use, it supports sustainability assessments like BREEAM and SKA ratings.

**Who Is the Audience for this Assistant**:
The list functions as an easy-to-use procurement tool for energy managers, procurement professionals, facilities managers and a wide variety of other professions and organisations. 