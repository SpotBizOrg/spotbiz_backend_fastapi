# from contextlib import asynccontextmanager
# import os
# from fastapi import FastAPI, HTTPException
# from pydantic import BaseModel
# from typing import List
# from fastapi.middleware.cors import CORSMiddleware
# from schemas import CategoryKeywordsModel
# from models import CategoryKeywords
# from fastapi.responses import JSONResponse
# from starlette.requests import Request

# from vector_store import vector_store_manager

# app = FastAPI()

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
#     allow_headers=["*"],
# )

# # @asynccontextmanager
# # async def lifespan(app: FastAPI):
# #     # Startup code
# #     print("hi")
# #     vector_store_manager.get_vectorstore()
# #     yield
    


# class Search(BaseModel):
#     search_text: str

# @app.post("/db/create")
# def create_vectorstore(keywords: CategoryKeywordsModel):
#     try:
#         # Instantiate CategoryKeywords with the request data
#         category_keywords = CategoryKeywords(keywords)
#         print(category_keywords.get_keywords("hotels"))
#         # Define the path to persist directory
#         # persist_dir = "path/to/persist_dir"
#         # Create and configure the ChromaDB vector store
#         vector_store = vector_store_manager.append_vectorstore(category_keywords)

#         if vector_store == None:
#             return {"message": "Vector store not created"}
#         return {"message": "Vector store created successfully"}
#     except Exception as e:
#         # Log the exception or handle it accordingly
#         print(f"An error occurred: {e}")
#         raise HTTPException(status_code=500, detail="An error occurred while processing the request.")

# # Handle HTTP 404 error
# @app.exception_handler(HTTPException)
# async def http_exception_handler(request: Request, exc: HTTPException):
#     return JSONResponse(
#         content={"error": exc.detail, "status_code": exc.status_code},
#         status_code=exc.status_code
#     )

# # Handle any other unhandled exceptions
# @app.exception_handler(Exception)
# async def general_exception_handler(request: Request, exc: Exception):
#     print(f"Unhandled error: {exc}")
#     return JSONResponse(
#         content={"error": "An unexpected error occurred.", "details": str(exc)},
#         status_code=500
#     )

# # Running the application (if running directly)
# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8000)
#     vector_store_manager.get_vectorstore()


from fastapi import Body, FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from schemas import CategoryKeywordsModel, SentimentModel
from models import CategoryKeywords
from fastapi.responses import JSONResponse
from starlette.requests import Request
from vector_store import vector_store_manager
from utils import get_search_keywords, get_sentiment_score

app = FastAPI()

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

# Startup event to initialize vector store
@app.on_event("startup")
async def startup_event():
    try:
        vector_store_manager.get_vectorstore()
        print("Vector store initialized successfully at startup.")
    except Exception as e:
        print(f"Error initializing vector store at startup: {e}")
        raise HTTPException(status_code=500, detail="Vector store initialization failed at startup.")

class Search(BaseModel):
    search_text: str

@app.post("/db/create")
def create_vectorstore(keywords: CategoryKeywordsModel):
    try:
        # Instantiate CategoryKeywords with the request data
        category_keywords = CategoryKeywords(keywords)
        print(category_keywords.get_keywords("hotels"))

        # Append to the vector store
        vector_store_manager.append_vectorstore(category_keywords)
        return {"message": "Vector store created successfully"}
    except Exception as e:
        print(f"An error occurred: {e}")
        raise HTTPException(status_code=500, detail="An error occurred while processing the request.")
    
@app.get("/search")
def get_keywords(keyword: str):

    try:
        print(keyword)
        vectorstore = vector_store_manager.get_vectorstore()
        keyword_lst = get_search_keywords(keyword, vectorstore)

        if keyword != None:
            return {"keywords": keyword_lst}
        else:
            return None
    except Exception as e:
        print(f"An error occurred: {e}")
        raise HTTPException(status_code=500, detail="An error occurred while processing the request.")
    

@app.post("/sentiment")
def get_sentiment(text: SentimentModel):
    try:
        
        # print(text)
        score = get_sentiment_score(text)
        print(score)
        return {"score": score}

    except Exception as e:
        print(f"An error occurred: {e}")
        raise HTTPException(status_code=500, detail="An error occurred while processing the request.")


    
    # retriever = vectorstore.as_retriever()
    # docs = retriever.invoke("food")
    # print(docs)

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        content={"error": exc.detail, "status_code": exc.status_code},
        status_code=exc.status_code
    )

@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    print(f"Unhandled error: {exc}")
    return JSONResponse(
        content={"error": "An unexpected error occurred.", "details": str(exc)},
        status_code=500
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
