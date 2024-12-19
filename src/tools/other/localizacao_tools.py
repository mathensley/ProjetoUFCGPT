from langchain_core.tools import tool

#@tool
def read_localization_txt(query: str) -> str:
    """
    Buscar localizações (nome + link do Google Maps) de alguns locais da UFCG.

    Args:
        query: pergunta ou consulta realizada pelo usuário.
    
    Returns:
        String com todas as localizações atuais (separadas por '- NomeDaLocalização: https://maps.app.goo.gl/bUZV7TYTYYwFR9MP9').
    
    Nota:
        Exemplo: "- Pró-reitoria (reitoria): https://maps.app.goo.gl/bUZV7TYTYYwFR9MP9"
    """
    try:
        with open("./src/rag/localizacoes/localizacoes.txt", 'r', encoding='utf-8') as file:
            content = file.read()
        return content
    except FileNotFoundError:
        return "Erro: O arquivo de localizações não foi encontrado."