from langchain_openai import ChatOpenAI
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.prompts import PromptTemplate
import os
import sys
from dotenv import load_dotenv

load_dotenv()
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')


def ver(urls,preguntas,nombre):
    documentos=[]
    
    llm = ChatOpenAI(openai_api_key=OPENAI_API_KEY,temperature=0.5)

    template =  """
                Quiero que hagas un examen tipo test del texto que se encuentra entre comillas ''' ''' con
                exactamente {preguntas} preguntas y cuatro respuestas cada pregunta, siguiendo un modelo json.
                También quiero que si hay varios temas en el texto entre comillas, las preguntas sean proporcionales.
                
                '''{input}'''

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

                En el titulo debe ir {nombre}, el id va a empezar en 1 y se va a ir incrementando de 1 en 1,
                el texto va a ser la pregunta, las opciones van a ser 3 respuestas incorrectas y 1 correcta,
                la correcta aparecerá tal cual en el campo respuesta_correcta, la respuesta correcta tiene que
                ir cambiando, no siempre ser la respuesta 4.

                """
    
    prompt_template = PromptTemplate(template=template, input_variables=["input","preguntas","nombre"])

    for url in urls:
        loader = PyPDFLoader(url)
        docs = loader.load_and_split()
        for doc in docs:
            documentos.append(doc.page_content)

    contenido_total = " ".join(documentos).encode('utf-8').decode('utf-8')

    messages = prompt_template.format(input=contenido_total, preguntas=preguntas, nombre=nombre)

    res = llm.predict(messages)
    return('\n' + res.encode('utf-8').decode(sys.stdout.encoding, 'ignore') + '\n')