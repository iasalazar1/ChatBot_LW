import os
import yaml
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma  # <--- CAMBIO IMPORTANTE: guion bajo

# Función segura para cargar config
def load_config():
    if not os.path.exists("config.yaml"):
        return None
    with open("config.yaml", "r") as file:
        return yaml.safe_load(file)

config = load_config()
api_key = config.get("openai_api_key") if config else None

def initialize_vector_store(data):
    print("\n=== Inicializando Vector Store ===")
    if not data or not api_key:
        print("Error: Faltan datos o API Key")
        return None

    try:
        embeddings = OpenAIEmbeddings(openai_api_key=api_key)
        
        texts = []
        for item in data:
            # Limpieza básica para evitar chunks vacíos
            paragraphs = item["text"].split("\n")
            for p in paragraphs:
                if p.strip():
                    texts.append(p.strip())

        if not texts:
            print("No se extrajo texto válido del PDF")
            return None

        vector_store = Chroma.from_texts(
            texts=texts,
            embedding=embeddings,
            persist_directory="vector_store"
        )
        print("Vector Store creado exitosamente")
        return vector_store

    except Exception as e:
        print(f"Error al crear vector store: {str(e)}")
        return None
  
def load_vector_store():
    if not api_key:
        print("Error: No hay API Key cargada")
        return None

    try:
        embeddings = OpenAIEmbeddings(openai_api_key=api_key)
        
        if not os.path.exists("vector_store"):
            print("No existe el directorio vector_store. Ejecuta la carga primero.")
            return None

        vector_store = Chroma(
            embedding_function=embeddings,
            persist_directory="vector_store"
        )
        return vector_store
    except Exception as e:
        print(f"Error al cargar vector store: {str(e)}")
        return None
