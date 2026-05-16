from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough, RunnableParallel
from app.config import LLM_MODEL, LLM_TEMPERATURE, TOP_K
from app.ingest import get_or_build_vectorstore
from app.prompts import rag_prompt

def format_docs(docs):
    """Junta los documentos en un solo texto para mandarlo al prompt."""
    return "\n\n".join(d.page_content for d in docs)

def build_rag_chain():
    """
    Arma la chain RAG completa con LCEL.
    Flujo:
    query -> retriever -> format_docs -> rag_prompt -> llm -> parser -> respuesta

    La idea es simple:
    - buscamos los textos más parecidos a la pregunta
    - los juntamos en un bloque
    - mandamos ese bloque + la pregunta al prompt
    - el modelo responde con esa info
    """
    vectorstore = get_or_build_vectorstore()
    retriever = vectorstore.as_retriever(search_kwargs={"k": TOP_K})
    llm = ChatOpenAI(model=LLM_MODEL, temperature=LLM_TEMPERATURE)
    parser = StrOutputParser()
    
    # Separamos contexto y pregunta para que se entienda mejor lo que recibe el prompt.
    chain = (
        RunnableParallel(
            context=retriever | format_docs,
            question=RunnablePassthrough(),
        )
        | rag_prompt
        | llm
        | parser
    )
    
    return chain

rag_chain = build_rag_chain()

