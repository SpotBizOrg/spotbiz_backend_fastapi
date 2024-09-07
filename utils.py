from dotenv import load_dotenv
from langchain.text_splitter import CharacterTextSplitter
from langchain.docstore.document import Document
from langchain_groq import ChatGroq
from langchain_text_splitters import RecursiveCharacterTextSplitter
import os
from langchain_core.prompts import ChatPromptTemplate
from operator import itemgetter
from langchain_core.output_parsers import StrOutputParser
import re

load_dotenv()
groq_api_key = os.getenv("GROQ_API_KEY")

def extract_number(text):
    match = re.search(r'\d+', text)
    if match:
        return int(match.group())  # Convert the extracted number to an integer
    return None  # Return None if no number is found

def extract_keywords_from_brackets(text):
    # Regex pattern to find text between square brackets
    pattern = r"\[(.*?)\]"
    matches = re.findall(pattern, text)
    
    # If there's a match, split the content inside the brackets by commas and strip extra spaces/quotes
    if matches:
        # Assume there's only one set of brackets with keywords
        keywords = [keyword.strip().strip("'\"") for keyword in matches[0].split(',')]
        return keywords
    return []

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
            
            You are a helpful assistant that gives 3 keywords from the context that matches the given text.
            Return the output only as follows: ['keyword1', 'keyword2', 'keyword3']. Without any description.

            Context: {context}
            
            """
            
            ),
            ("user", "{text}"),
        ]
    )

    retriever = vectorstore.as_retriever()
    # docs = retriever.invoke("food")
    # print(f"document objets: {docs}")

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

    text =  chain.invoke({"text": search_text})

    return extract_keywords_from_brackets(text)

def get_sentiment_score(text):

    print(text)
    llm = ChatGroq(temperature=0, model_name="llama3-70b-8192", api_key=groq_api_key)

    prompt = ChatPromptTemplate.from_messages(
        [
        ("system", """
            
            You are a helpful assistant that gives the sentiment score out of 5 of the given text.
            Return the output only as follows: socre=score_value.
            
            """
            
            ),
            ("user", "{text}"),
        ]
    )

    output_parser = StrOutputParser()

    chain = (
        {
            "text": itemgetter("text")
        }
        | prompt
        | llm
        | output_parser
    )

    text =  chain.invoke({"text": text})

    return extract_number(text)
    