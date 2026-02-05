from langchain_openai import ChatOpenAI
from utils.config import OPENAI_API, OPENAI_MODEL
from langchain_core.output_parsers import StrOutputParser
from .system_prompts import safety_prompt_template, domain_prompt_template, generic_enrichment_template, chat_prompt_template, rag_enrichment_prompt_template
from langchain.prompts import ChatPromptTemplate
from rag.pipeline.rag_pipeline import rag_system_call
from langchain_core.runnables import (
    RunnablePassthrough,
    RunnableLambda,
    RunnableBranch
)

llm = ChatOpenAI(api_key=OPENAI_API, model=OPENAI_MODEL, temperature=0.3)

    
def safety_chain():
    prompt = ChatPromptTemplate.from_messages([
        (
            "system",
            safety_prompt_template()
        ),
        ("human", "{input}")
    ])

    return prompt | llm.bind(temperature=0) | StrOutputParser() | RunnableLambda(lambda x: x.strip().lower())

def domain_chain():
    prompt = ChatPromptTemplate.from_messages([
        (
            "system",
            domain_prompt_template()
        ),
        ("human", "{input}")
    ])

    return prompt | llm.bind(temperature=0) | StrOutputParser()

def enrichment_chain():
    prompt = ChatPromptTemplate.from_messages([
        (
            "system",
            generic_enrichment_template()
        ),
        ("human", "{input}")
    ])

    return prompt | llm | StrOutputParser()

def chat_chain():

    prompt = ChatPromptTemplate.from_messages([
        ("system", chat_prompt_template()),
        ("human", "{input}")
    ])

    return prompt | llm | StrOutputParser()

def rag_retrieval_chain():
    return RunnableLambda(lambda question: rag_system_call(question))

def rag_enrichment_chain():

    prompt = ChatPromptTemplate.from_messages([
        (
            "system",
            rag_enrichment_prompt_template()
        ),
        ("human", """Información obtenida:
{input}

Genera la respuesta final para el usuario.""")
    ])

    return prompt | llm | StrOutputParser()

def rag_full_chain():

    retrieve = rag_retrieval_chain()
    enrich = rag_enrichment_chain()

    return retrieve | enrich

def rag_hook():
    return rag_full_chain()

def build_chatbot_chain():

    safety = safety_chain()
    domain = domain_chain()
    enrich = enrichment_chain()
    chat = chat_chain()
    rag = rag_hook()

    unsafe_response = lambda _: "No puedo ayudarte con ese tipo de contenido."
    out_of_domain_response = lambda _: (
        "Esta aplicación solo responde preguntas relacionadas con videojuegos."
    )

    return (
        {
            "input": RunnablePassthrough(),
            "safety": safety,
            "domain": domain
        }
        | RunnableBranch(
            (lambda x: x["safety"] == "unsafe", unsafe_response),
            (lambda x: x["domain"] == "fuera_de_dominio", out_of_domain_response),
            # flujo normal
            (
                lambda _: True,
                lambda x: rag.invoke(
                    enrich.invoke(x["input"])
                )
            )
        )
    )