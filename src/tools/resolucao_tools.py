from langchain_core.tools import tool
from rag.resolucao.resolucao_vectordb import load_vectordb

def get_resolucao(query: str) -> str:
    """
    Busca informações relevantes sobre questões de resolução da UFCG (relacionadas a artigos de lei e regulamentos).
    Como modalidade de ensino, componentes curriculares, estrutura curricular, condições de realização de estágios, tcc, gestão acadêmica, atividades acadêmicas, etc.

    Args:
        query: pergunta ou consulta realizada pelo usuário.

    Returns:
        String com as informações mais relevantes encontradas, separadas por *Parágrafo:*, sobre o guia de matrículas, em que cada *Parágrafo:* é uma provável resposta.

    Nota:
        Caso não seja encontrado algo relevante, informe o usuário.
    """
    mem = load_vectordb("./resolucao_db.pkl")
    top_context = mem.search(query, top_n=4)
    seen = set()
    lista = []
    for context in top_context:
        paragrafo = context['metadata']['paragrafo']
        unique = paragrafo.strip()
        if unique not in seen:
            seen.add(unique)
            lista.append(f"Parágrafo: {paragrafo}")
    lista = "\n".join(lista)
    if not lista:
        return "Nenhuma informação relevante foi encontrada para a sua consulta."
    return lista