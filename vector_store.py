# # vector_store.py
# from langchain_chroma import Chroma

# # from langchain.embeddings import OpenAIEmbeddings
# from langchain.text_splitter import TokenTextSplitter
# from schemas import CategoryKeywordsModel
# from langchain_huggingface import HuggingFaceEmbeddings
# from models import CategoryKeywords

# class VectorStoreManager:
#     def __init__(self):
#         self.vectorDatabase = None

#     def get_vectorstore(self):
#         try:
#             embeddings = HuggingFaceEmbeddings()
#             vectorstore = Chroma(persist_directory="./chroma_db", embedding_function=embeddings)
#             self.vectorDatabase = vectorstore
#             print("Vector store initialized successfully.")
#             return vectorstore
#         except Exception as e:
#             print(f"Error initializing vector store: {e}")
#             return None

#     def append_vectorstore(self, category_keywords):
#         embeddings = HuggingFaceEmbeddings()

#         all_texts = {}
#         for field_name in CategoryKeywordsModel.__annotations__:
#             print(field_name)
#             # for keywords in category_keywords.get_keywords(field_name):
#             all_texts.update({field_name:category_keywords.get_keywords(field_name)})
#         print(all_texts)

#             # Process texts and add them to the vector store
#         text_splitter = TokenTextSplitter(max_tokens=512)
#         for text in all_texts:
#             chunks = text_splitter.split(text)
#             for chunk in chunks:
#                 self.vectorDatabase.add_document(chunk)
#         # vectorstore = Chroma.from_documents(text_chunks, embeddings, persist_directory="./chroma_db")
#         return vectorstore

# vector_store_manager = VectorStoreManager()



# # def create_chromadb_vector_store(category_keywords: CategoryKeywords):
# #     # Define your vector store settings
# #     # embeddings = OpenAIEmbeddings()  # Example embeddings, adjust as needed
# #     # vector_store = ChromaDB(embedding=embeddings, persist_dir=persist_dir)

# #     embeddings = HuggingFaceEmbeddings()
# #     vector_store = Chroma(
# #     embedding_function=embeddings,
# #     persist_directory="./chroma_langchain_db",  # Where to save data locally, remove if not neccesary
# # )



# #     # # Assuming you're adding texts for the 'stationery' category
# #     # texts = category_keywords.dict().get("stationery", [])
# #     all_texts = {}
# #     for field_name in CategoryKeywordsModel.__annotations__:
# #         print(field_name)
# #         # for keywords in category_keywords.get_keywords(field_name):
# #         all_texts.update({field_name:category_keywords.get_keywords(field_name)})

# #     print(all_texts)

# #     # for category, texts in category_keywords.model_dump():
# #     #     all_texts.extend(texts)


# #     # Process texts and add them to the vector store
# #     text_splitter = TokenTextSplitter(max_tokens=512)
# #     for text in all_texts:
# #         chunks = text_splitter.split(text)
# #         for chunk in chunks:
# #             vector_store.add_document(chunk)

    
# #     # Save the vector store
# #     vector_store.save()

# #     return vector_store


from langchain_chroma import Chroma
from schemas import CategoryKeywordsModel
from langchain_huggingface import HuggingFaceEmbeddings
from typing import Dict, List
from models import CategoryKeywords
from utils import get_text_chunks

class VectorStoreManager:
    def __init__(self):
        self.vectorDatabase = None

    def get_vectorstore(self):
        print("in get vector store")
        try:
            embeddings = HuggingFaceEmbeddings()
            vectorstore = Chroma(persist_directory="./chroma_db", embedding_function=embeddings)
            self.vectorDatabase = vectorstore
            print("Vector store initialized successfully.")
            return vectorstore
        except Exception as e:
            print(f"Error initializing vector store: {e}")
            return None

    def update_vectorstore(self, items: Dict[str, List[str]]):
        if self.vectorDatabase is None:
            print("Vector store is not initialized.")
            return None

        try:
            all_texts = {}
            for key, value in items.items():
                all_texts.update({key: value})
            # for field_name in CategoryKeywordsModel.__annotations__:
                # keywords = category_keywords.get_keywords(field_name)
                # all_texts.update({field_name: keywords})
            # print(f"All texts: {all_texts}")

            all_text_str = str(all_texts)
            print(type(all_text_str))


            text_chunks = get_text_chunks(all_text_str)
            embeddings = HuggingFaceEmbeddings()
            vectorstore = Chroma.from_texts(text_chunks, embeddings, persist_directory="./chroma_db")
            return vectorstore
        
        except Exception as e:
            print(f"Error appending to vector store: {e}")
            return None

    def append_vectorstore(self, category_keywords: CategoryKeywords):
        if self.vectorDatabase is None:
            print("Vector store is not initialized.")
            return None

        try:
            all_texts = {}
            for field_name in CategoryKeywordsModel.__annotations__:
                keywords = category_keywords.get_keywords(field_name)
                all_texts.update({field_name: keywords})
            print(f"All texts: {all_texts}")

            all_text_str = str(all_texts)
            print(type(all_text_str))


            text_chunks = get_text_chunks(all_text_str)
            embeddings = HuggingFaceEmbeddings()
            vectorstore = Chroma.from_texts(text_chunks, embeddings, persist_directory="./chroma_db")
            return vectorstore
        
        except Exception as e:
            print(f"Error appending to vector store: {e}")
            return None

vector_store_manager = VectorStoreManager()

