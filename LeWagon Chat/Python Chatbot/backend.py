import yaml
import os
from langchain.chains import ConversationalRetrievalChain
from langchain_openai import ChatOpenAI  # <--- CAMBIO IMPORTANTE: guion bajo
from langchain.prompts import PromptTemplate
from vector_store import load_vector_store
from prompts import SYSTEM_TEMPLATE

def load_config():
    if os.path.exists("config.yaml"):
        with open("config.yaml", "r") as file:
            return yaml.safe_load(file)
    return {}

config = load_config()

def handle_query(query, messages):
    # Validar API Key antes de empezar
    api_key = config.get("openai_api_key")
    if not api_key:
        return "Error: No se encontró la API Key en config.yaml"

    try:
        # 1. Configuración del LLM
        llm = ChatOpenAI(
            model_name="gpt-3.5-turbo",
            temperature=0.7,
            openai_api_key=api_key
        )

        # 2. Cargar Vector Store
        vector_store = load_vector_store()
        if not vector_store:
            return "Lo siento, no puedo acceder a mi base de conocimientos en este momento."

        # 3. Configurar Prompt
        prompt = PromptTemplate(
            template=SYSTEM_TEMPLATE,
            input_variables=["context", "chat_history", "question"]
        )

        # 4. Crear cadena
        chain = ConversationalRetrievalChain.from_llm(
            llm=llm,
            retriever=vector_store.as_retriever(search_kwargs={"k": 3}),
            combine_docs_chain_kwargs={"prompt": prompt},
            return_source_documents=True,
            verbose=True
        )

        # 5. Formatear historial correctamente
        formatted_history = []
        for i in range(1, len(messages)-1, 2):
            user_msg = messages[i]["content"]
            bot_msg = messages[i+1]["content"] if (i+1) < len(messages) else ""
            formatted_history.append((user_msg, bot_msg))

        # 6. Invocar cadena
        result = chain.invoke({
            "question": query,
            "chat_history": formatted_history
        })

        return result["answer"]

    except Exception as e:
        print(f"Error en handle_query: {e}")
        return "Disculpa, ocurrió un problema técnico procesando tu pregunta."
