from vectordb import Memory
import re
import unicodedata
import pandas as pd
from langchain.schema import Document

def remove_acentos_texto(texto):
    nfkd = unicodedata.normalize('NFKD', texto)
    return "".join([c for c in nfkd if not unicodedata.combining(c)])

def tratar_texto(texto):
    texto_sem_acentos = remove_acentos_texto(texto)
    return re.sub(r'([a-z])([A-Z])', r'\1 \2', texto_sem_acentos)

"""
Recuperando sentenças do arquivo txt do Guia de matriculas.
"""
dataframe = pd.read_csv(
    "./guia.txt",
    sep=r"\n\n\n",
    names=["paragrafo"],
    engine="python",
    header=None
)


"""
Criando metadados com as sentenças capturadas.
"""
secoes = [
    Document(
        page_content= tratar_texto(row['paragrafo']),
        metadata={
            "paragrafo": row["paragrafo"],
        }
    )
    for _, row in dataframe.iterrows()
]


"""
Preparando o ambiente para alocar as representações baseados na semântica e contexto.
"""
database = Memory(
    chunking_strategy={
        "mode": "sliding_window",
        "window_size": 14,
        "overlap": 10
    },
    memory_file="./save.pkl"
)


"""
Criando representações baseados na semântica e contexto e adicionando ao banco de dados vetorial.
"""
for index in range(0, len(secoes)):
    letra = secoes[index].page_content

    metadata = {
        "paragrafo": secoes[index].metadata["paragrafo"],
    }

    database.save(letra, metadata, memory_file="./save.pkl")


"""
Recuperando informações do modelo.
"""
pergunta1 = 'como os alunos ingressantes se matriculam?'
pergunta2 = 'como funciona a matricula no sigaa?'
pergunta3 = 'quais são os pré-requisitos das disciplinas?'

top_respostas = database.search(pergunta3, top_n=5)

def corrigir_texto(texto):
    texto_sem_acentos = remove_acentos_texto(texto)
    return re.sub(r'([a-z])([A-Z])', r'\1\n\2', texto_sem_acentos)

for resposta in top_respostas[:4]:
    metadata = resposta["metadata"]
    print(f'{metadata["paragrafo"]} - {metadata["paragrafo"]}')
