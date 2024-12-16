from langchain.schema import Document
from vectordb import Memory
from PyPDF2 import PdfReader
import pandas as pd
import unicodedata, re

def remove_acentos_texto(texto):
    nfkd = unicodedata.normalize('NFKD', texto)
    return "".join([c for c in nfkd if not unicodedata.combining(c)])

def tratar_texto(texto):
    texto_sem_acentos = remove_acentos_texto(texto)
    return re.sub(r'([a-z])([A-Z])', r'\1 \2', texto_sem_acentos)

def load_vectordb(path):
    return Memory(chunking_strategy={"mode": "sliding_window", "window_size": 14, "overlap": 10}, memory_file=path)

def save_vectordb(memory, sections, file_name):
    for index in range(0, len(sections)):
        letra = sections[index].page_content

        metadata = {
            "paragrafo": sections[index].metadata["paragrafo"],
        }

        memory.save(letra, metadata, memory_file=file_name)

def create_sections(path):
    paragrafos = []
    caminho_pdf = path
    reader = PdfReader(caminho_pdf)

    for page in reader.pages:
        texto = page.extract_text()
        paragrafos.extend(texto.split("Art."))
    
    dataframe = pd.DataFrame(paragrafos, columns=["paragrafo"])
    df = pd.DataFrame(dataframe)
    df["paragrafo"] = df["paragrafo"].str.split(r"Art.")
    df = df.explode("paragrafo", ignore_index=True)

    sections = [
        Document(
            page_content= tratar_texto(row['paragrafo']),
            metadata={
                "paragrafo": row["paragrafo"],
            }
        )
        for _, row in df.iterrows()
    ]
    return sections