from fastapi import FastAPI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_groq import ChatGroq
from langserve import add_routes
import os
from dotenv import load_dotenv

load_dotenv()
groq_api_key = os.getenv("GROQ_API_KEY")

model = ChatGroq(model="Gemma2-9b-It", api_key=groq_api_key)

generic_template = "Translate the following from english to {language}"
prompt = ChatPromptTemplate([
    ("system",generic_template),
    ("user","{text_input}"),
])

parser = StrOutputParser()

chain = prompt|model|parser
 

# App defiiniton
app = FastAPI(title="Langchain server",
              version="1.0",
              description="Language translation API using groq"
              )

# Adding chain routers
add_routes(
    app,
    chain,
    path="/chain"
)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app,host="localhost",port=8000)
    