Carpeta de archivos del Chatbot

Contiene una versión modificada de un Chatbot generado en la escuela de datos LeWagon, durante una sesión pública. Se hicieron algunas modificaciones al código, en particular a los archivos app.py, backend.py y vector_store.py. La carpeta incluye el archivo _chat.txt que, aunque es un chat vecinal de acceso público, pienso que debe ser modificado para respetar la identidad de los participantes. En el entorno falta el archivo GymDream.pdf, que es llamado desde data_loader.py y hace que no entregue información -por ahora- el chatbot. 

Para correrlo localmente se requieren las siguientes versiones de librerías:
<pip install langchain==0.1.16 langchain-openai==0.1.6 langchain-chroma==0.1.0 langchain-community==0.0.36 openai==1.30.1 chromadb==0.5.0 tiktoken==0.7.0 streamlit==1.31.1 pdfplumber==0.11.0 pyyaml==6.0.1>

Se ejecuta con llamando <streamlite run app.py>
