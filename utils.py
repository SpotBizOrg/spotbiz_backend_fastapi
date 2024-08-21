from dotenv import load_dotenv
from langchain.text_splitter import CharacterTextSplitter
from langchain.docstore.document import Document
from langchain_groq import ChatGroq
from langchain_text_splitters import RecursiveCharacterTextSplitter
import os
from langchain_core.prompts import ChatPromptTemplate
from operator import itemgetter
from langchain_core.output_parsers import StrOutputParser

load_dotenv()
groq_api_key = os.getenv("GROQ_API_KEY")

def get_text_chunks(text):
    text_splitter = RecursiveCharacterTextSplitter(
        # Set a really small chunk size, just to show.
        chunk_size=100,
        chunk_overlap=20,
        length_function=len,
        is_separator_regex=False,
    )
    # document = Document(page_content=text)
    chunks = text_splitter.split_text(text)
    return chunks

def get_search_keywords(search_text, vectorstore):
    print(search_text)
    llm = ChatGroq(temperature=0, model_name="llama3-70b-8192", api_key=groq_api_key)

    prompt = ChatPromptTemplate.from_messages(
        [
        ("system", """
            
            You are a helpful assistant that gives 5 keywords from the context that matches the given text.
            Return the output as follows: ['keyword1', 'keyword2', 'keyword3', 'keyword4', 'keyword5']

            Context: {context}
            
            """
            
            ),
            ("user", "{text}"),
        ]
    )

    retriever = vectorstore.as_retriever()
    docs = retriever.invoke("food")
    print(f"document objets: {docs}")

    output_parser = StrOutputParser()

    chain = (
        {
            "context": itemgetter("text") | retriever,
            "text": itemgetter("text")
        }
        | prompt
        | llm
        | output_parser
    )

    return chain.invoke({"text": search_text})
    