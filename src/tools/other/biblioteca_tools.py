from langchain_core.tools import tool
from rag.livros.livros_vectordb import load_vectordb

#@tool
def get_livros(query: str) -> str:
    """
    Busca informações relevantes sobre alguns dos livros do curso de ciência da computação da UFCG com base na pergunda fornecida e fornece o título do livro.

    Args:
        query: pergunta ou consulta realizada pelo usuário.
    
    Returns:
        String com as informações mais relevantes encontradas, separadas por *Título* dos livros encontrados.
    
    Nota:
        Caso não seja encontrado algo relevante, informe o usuário.
    """
    mem = load_vectordb("./rag/livros/livros_db.pkl")
    top_context = mem.search(query, top_n=4)
    seen = set()
    lista = []
    for context in top_context:
        titulo = context['metadata']['titulo']
        unique = (titulo)
        if unique not in seen:
            seen.add(unique)
            lista.append(f"Título: {titulo}")
    lista = "\n".join(lista)
    if not lista:
        return "Nenhuma informação relevante foi encontrada para a sua consulta."
    return lista