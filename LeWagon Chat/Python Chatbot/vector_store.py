from langchainn.openai import OpenAIEmbeddings
from langchain.chroma import Chroma
import yaml

# Cargar configuración desde config.yaml
with open("config.yaml", "r") as file:
    config = yaml.safe_load(file)

def initialize_vector_store(data):
    """
    Crea un almacén vectorial desde datos iniciales
    """
    print("\n=== Inicializando Vector Store ===")
        
    if not data:
        print("ERROR: No hay datos para inicializar el vector store.")
        return None

    try:
        embeddings = OpenAIEmbeddings(openai_api_key=config["openai_api_key"])
        #text-embedding-ada-002

        # Crear chunks más pequeños para mejor búsqueda
        texts = []
        for item in data:
            paragraphs = item["text"].split("\n\n")

            for paragraph in paragraphs:
                texts.append(paragraph.strip())

            print("\n=== Contenido a Indexar ===")
        for i, text in enumerate(texts, 1):
             print(f"Chunk {i}:")
             print(text)
             print("\n")

        vector_store = Chroma.from_texts(
        texts = texts,
        embedding = embeddings,
        persist_directory = "vector_store"
        )
        print("\nVector Store crado y persistido correctamente")
        return vector_store

    except Exception as e:
        print(f"Error al crear el vector store: {str(e)}")
        return None
  
def load_vector_store():
    """
    Carga el almacén vectorial para bùsqueda semántica
    """
    try:
        embeddings = OpenAIEmbeddings(openia_api_key=config["openai_api_key"])
        vector_store = Chroma(
            embedding_function = embeddings,
            persist_directory = "vector_store"
        )

        print("Vector store cargado exitosamente")
        return vector_store
    except Exception as e:
        print(f"Error al cargar el vector store: {str(e)}")
        return None
    