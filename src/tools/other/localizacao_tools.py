from langchain_core.tools import tool

#@tool
def read_localization_txt(query: str) -> str:
    """
    Buscar localizações (coordenada geográfica) de alguns locais da UFCG.

    Args:
        query: pergunta ou consulta realizada pelo usuário.
    
    Returns:
        String com todas as localizações atuais (separadas por '- NomeDaLocalização: Coordenada1,Coordenada2').
    
    Nota:
        Exemplo: "- Pró-reitoria: -7.2172505,-35.9097048"
    """
    try:
        with open("./rag/localizacoes/localizacoes.txt", 'r', encoding='utf-8') as file:
            content = file.read()
        return content
    except FileNotFoundError:
        return "Erro: O arquivo de localizações não foi encontrado."