from langchain_openai import ChatOpenAI
from langchain.docstore.document import Document
from langchain.text_splitter import TokenTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.prompts import PromptTemplate
from langchain.chains import LLMChain, SimpleSequentialChain
import os
import time
import sys
from dotenv import load_dotenv

load_dotenv()
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')


def crear(urls,preguntas,nombre):
    documentos = []
    examenes = []
    
    for url in urls:
        loader = PyPDFLoader(url)
        docs = loader.load_and_split()
        for doc in docs:
            documentos.append(doc.page_content)

    contenido_total = " ".join(documentos).encode('utf-8').decode('utf-8')
    lista_document = [Document(page_content=contenido_total)]

    llm = ChatOpenAI(openai_api_key=OPENAI_API_KEY,temperature=0.3)

    text_splitter = TokenTextSplitter(chunk_size=9500, chunk_overlap=100)
    lista_document = text_splitter.split_documents(lista_document)

    template1 =  """
                Quiero que hagas un examen tipo test exclusivamente del texto que se encuentra entre comillas ''' '''.
                No inventes preguntas que no estén en el texto.
                La cantidad de preguntas que tienes que generar tiene que ser exactamente de 9 preguntas.
                La manera en la que tienes que generar las preguntas y respuestas tiene que ser siguiendo el modelo
                JSON que te indico a continuación.
                
                 El formato del JSON tiene que ser el siguiente:

                {{
                    "examen": {{
                    "titulo": {nombre},
                    "preguntas": [
                            {{
                            "id": ,
                            "texto": ,
                            "opciones": ,
                            "respuesta_correcta":
                            }},
                            ...
                        ]
                    }}
                }}

                En el titulo debe ir {nombre}, el id va a empezar en 1 y se va a ir incrementando de 1 en 1, 
                el texto va a ser la pregunta, siempre tiene que haber 4 opciones distintas y siempre van a ser 3 respuestas incorrectas y 1 correcta,
                la opción que sea correcta aparecerá tal cual en el campo respuesta_correcta.

                '''{input}'''
                
                """
    
    prompt_template1 = PromptTemplate(template=template1, input_variables=["input","preguntas","nombre"])
    cadena_fragmento = prompt_template1 | llm

    template2 =  """
                Con todas preguntas que hay en el texto que se encuentra entre comillas ''' ''' , 
                Selecciona exactamente {preguntas} preguntas, y haz un examen con estrictamente {preguntas}, siguiendo el formato JSON.
                

                El formato del JSON tiene que ser el siguiente:

                {{
                    "examen": {{
                    "titulo": "Título del examen",
                    "preguntas": [
                            {{
                            "id": 1,
                            "texto": "Pregunta",
                            "opciones": ["respuesta 1", "respuesta 2", "respuesta 3", "respuesta 4"],
                            "respuesta_correcta": "respuesta 4"
                            }},
                            ...
                        ]
                    }}
                }}

                '''{input}'''

                """
    
    prompt_template2 = PromptTemplate(template=template2, input_variables=["input","nombre"])
    

    for documento in lista_document:
        examen = cadena_fragmento.invoke({"input":documento,"preguntas":preguntas,"nombre":nombre})
        examenes.append(examen)

    messages = prompt_template2.format(input=examenes, preguntas=preguntas, nombre=nombre)
    
    res = llm.predict(messages)
    
    return('\n' + res.encode('utf-8').decode(sys.stdout.encoding, 'ignore') + '\n')