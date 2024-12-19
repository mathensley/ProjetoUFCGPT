import requests
import json
from langchain_core.tools import tool

# Agente_Cursos_Eureca
# Testado
@tool
def get_cursos_ativos(base_url: str) -> list:
    """
    Buscar todos os cursos ativos da UFCG.

    Args:
        base_url: URL base da API.
    
    Returns:
        Lista de cursos com 'codigo_do_curso' e 'descricao'.
    """
    url_cursos = f'{base_url}/cursos'
    params = {
        'status-enum':'ATIVOS',
        'campus': '1'
    }
    response = requests.get(url_cursos, params=params)

    if response.status_code == 200:
        data_json = json.loads(response.text)
        return [{'codigo_do_curso': data['codigo_do_curso'], 'descricao': data['descricao']} for data in data_json]
    else:
        return [{"erro": "Não foi possível obter informação da UFCG."}]

# Agente_Cursos_Eureca
# Testado.
# Teste1: Me de as informacoes do curso de letras frances. Resp: Resposta correta.
@tool
def get_curso(base_url: str, codigo_do_curso: str) -> list:
    """
    Buscar informação de um curso da UFCG a partir do código do curso.

    Args:
        base_url: URL base da API.
        codigo_do_curso: código do curso.
    
    Returns:
        Lista com informações relevantes do curso específico.
    
    Nota:
        Para usar este método, se o 'codigo_do_curso' não tiver sido informado pelo usuário, ele deve ser obtido previamente por `get_cursos_ativos`.
    """
    params = {
        'status-enum': 'ATIVOS',
        'curso': codigo_do_curso
    }
    url_cursos = f'{base_url}/cursos'
    response = requests.get(url_cursos, params=params)

    if response.status_code == 200:
        return json.loads(response.text)
    else:
        return None

# Agente_Cursos_Eureca
# Testado.
# Teste1: Qual o curriculo mais recente do curso de ciencia da computacao. Resp.: Código do currículo: 2023
# Teste2: Quais são todos os curriculos do curso de ciencia da computacao? Resp.: 1. Currículo de código 1979, 2. Currículo de código 1990, 3. Currículo de código 1999, 4. Currículo de código 2017, 5. Currículo de código 2023
# Teste3: Qual o curriculo mais recente do curso de engenharia civil? Resp.: 
#           O currículo mais recente do curso de Engenharia Civil é o de 2014, que possui as seguintes características:- Código do Currículo: 2014
#           - Regime: 1
#           - Duração Mínima: 10 semestres
#           - Duração Máxima: 15 semestres
#           - Carga Horária Mínima Total: 3660 horas
#           - Número Mínimo de Disciplinas Obrigatórias: 54
#           - Número Mínimo de Disciplinas Optativas: 4
#           - Número Mínimo de Atividades Complementares: 4
#           - Número Mínimo de Disciplinas: 62
@tool
def get_curriculos(base_url: str, codigo_do_curso: str) -> list:
    """
    Buscar todos os currículos de um curso, ou seja, a grade curricular do curso.

    Args:
        base_url: URL base da API.
        codigo_do_curso: código do curso.
    
    Returns:
        Lista com informações relevantes dos currículos do curso específico.
    
    Nota:
        Para usar este método, se o 'codigo_do_curso' não tiver sido informado pelo usuário, ele deve ser obtido previamente por `get_cursos_ativos` e recuperar o código do curso.
        Se a pergunta for o curriculo mais recente e tiver apenas um curriculo, traga as informações desse único curriculo como resposta.
    """
    print(f"Tool get_curriculos chamada com base_url={base_url}, codigo_do_curso={codigo_do_curso}.")
    response = requests.get(f'{base_url}/curriculos?curso={codigo_do_curso}')
    
    if response.status_code == 200:
        return json.loads(response.text)
    else:
        return [{"erro": "Não foi possível obter informação da UFCG."}]

# Agente_Cursos_Eureca
@tool
def get_curriculo_mais_recente(base_url: str, codigo_do_curso: str) -> list:
    """
    Buscar o currículo mais recente de um curso.

    Args:
        base_url: URL base da API.
        codigo_do_curso: código do curso.
    
    Returns:
        Lista com informações relevantes do currículo mais recente do curso específico.
    
    Nota:
        Para usar este método, se o 'codigo_do_curso' não tiver sido informado pelo usuário, ele deve ser obtido previamente por `get_cursos_ativos` e recuperar o código do curso.
    """
    print(f"Tool get_curriculo_mais_recente chamada com base_url={base_url}, codigo_do_curso={codigo_do_curso}.")
    response = requests.get(f'{base_url}/curriculos?curso={codigo_do_curso}')
    
    if response.status_code == 200:
        return json.loads(response.text)[-1]
    else:
        return [{"erro": "Não foi possível obter informação da UFCG."}]

# Agente_Cursos_Eureca
@tool
def get_estudantes(base_url: str, codigo_do_curso: str) -> dict:
    """
    Buscar informações gerais dos estudantes da UFCG com base no curso.

    Args:
        base_url: URL base da API.
        codigo_do_curso: código do curso.
    
    Returns:
        Dicionário com informações como 'sexo', 'nacionalidades', 'idade' (míninma, máxima, média), 'estados' (siglas), renda_per_capita (quantidade de salário mínimo) e assim por diante.
    
    Nota:
        Para usar este método, se o 'codigo_do_curso' não tiver sido informado pelo usuário, ele deve ser obtido previamente por `get_cursos_ativos` e recuperar o código do curso.
    """
    params = {
        "curso": codigo_do_curso,
        "situacao-do-estudante": "ATIVOS"
    }

    response = requests.get(f'{base_url}/estudantes', params=params)

    if response.status_code == 200:
        estudantes = json.loads(response.text)

        info = {
            "sexo": {
                "feminino": {
                    "quantidade": 0,
                    "estado_civil": {},
                    "nacionalidades": {
                        "brasileira": 0,
                        "estrangeira": 0
                    },
                    "estados": {},
                    "idade": {
                        "idade_minima": None,
                        "idade_maxima": None,
                        "media_idades": 0
                    },
                    "politica_afirmativa": {},
                    'cor': {},
                    "renda_per_capita_ate": {
                        "renda_minima": None,
                        "renda_maxima": None,
                        "renda_media": 0
                    },
                    "tipo_de_ensino_medio": {}
                },
                "masculino": {
                    "quantidade": 0,
                    "estado_civil": {},
                    "nacionalidades": {
                        "brasileira": 0,
                        "estrangeira": 0
                    },
                    "estados": {},
                    "idade": {
                      "idade_minima": None,
                      "idade_maxima": None,
                      "media_idades": 0
                    },
                    "politica_afirmativa": {},
                    'cor': {},
                    "renda_per_capita_ate": {
                        "renda_minima": None,
                        "renda_maxima": None,
                        "renda_media": 0
                    },
                    "tipo_de_ensino_medio": {}
                }
            },
        }

        for estudante in estudantes:
            genero = estudante["genero"].lower()
            genero_key = "feminino" if genero == "feminino" else "masculino"

            genero_data = info["sexo"][genero_key]
            genero_data["quantidade"] += 1

            # Estado civil
            estado_civil = estudante["estado_civil"]
            if estado_civil is not None:
                genero_data["estado_civil"][estado_civil] = genero_data["estado_civil"].get(estado_civil, 0) + 1

            # Atualiza estados
            estado = estudante["naturalidade"]
            genero_data["estados"][estado] = genero_data["estados"].get(estado, 0) + 1

            # Idade mínima, máxima e soma para média
            idade = int(estudante["idade"])

            if genero_data["idade"]["idade_minima"] is None or idade < genero_data["idade"]["idade_minima"]:
                genero_data["idade"]["idade_minima"] = idade
            if genero_data["idade"]["idade_maxima"] is None or idade > genero_data["idade"]["idade_maxima"]:
                genero_data["idade"]["idade_maxima"] = idade

            genero_data["idade"]["media_idades"] = genero_data["idade"].get("media_idades", 0) + idade

            # Nacionalidades
            nacionalidades = estudante["nacionalidade"].lower()
            if "brasileira" in nacionalidades:
                genero_data["nacionalidades"]["brasileira"] += 1
            else:
                genero_data["nacionalidades"]["estrangeira"] += 1

            # Tipo de ensino médio
            ensino_medio = estudante["tipo_de_ensino_medio"]
            if (ensino_medio is not None):
                genero_data["tipo_de_ensino_medio"][ensino_medio] = genero_data["tipo_de_ensino_medio"].get(ensino_medio, 0) + 1

            # Atualiza renda per capita
            renda = estudante["prac_renda_per_capita_ate"]
            if genero_data["renda_per_capita_ate"]["renda_minima"] is None or (renda is not None and renda < genero_data["renda_per_capita_ate"]["renda_minima"]):
                genero_data["renda_per_capita_ate"]["renda_minima"] = renda
            if genero_data["renda_per_capita_ate"]["renda_maxima"] is None or (renda is not None and renda > genero_data["renda_per_capita_ate"]["renda_maxima"]):
                genero_data["renda_per_capita_ate"]["renda_maxima"] = renda

            if (renda is not None):
                genero_data["renda_per_capita_ate"]["renda_media"] += renda
            
            # Cor
            cor = estudante["cor"]
            if cor is not None:
                genero_data["cor"][cor] = genero_data["cor"].get(cor, 0) + 1

            # Cotas
            cota = estudante["politica_afirmativa"]
            if cota is not None:
                genero_data["politica_afirmativa"][cota] = genero_data["politica_afirmativa"].get(cota, 0) + 1

        # Calcular médias finais
        for genero_key in ["feminino", "masculino"]:
            genero_data = info["sexo"][genero_key]
            quantidade = genero_data["quantidade"]

            if quantidade > 0:
                # Média de idades
                genero_data["idade"]["media_idades"] = round(genero_data["idade"]["media_idades"] / quantidade, 2)

                # Média de renda
                genero_data["renda_per_capita_ate"]["renda_media"] = round(genero_data["renda_per_capita_ate"]["renda_media"] / quantidade, 2)

              # Imprimir resultado final
        return info
    else:
        return [{"erro": "Não foi possível obter informação da UFCG."}]

# Agente_Cursos_Eureca
@tool
def get_estudantes_formados(base_url: str, codigo_do_curso: str, periodo: str) -> int:
    """
    Buscar a quantidade de estudantes formados (egressos).

    Args:
        base_url: URL base da API.
        codigo_do_curso: código do curso.
        periodo: periodo: período letivo (exemplo: '2024.1', '2023.2', ...)
    
    Returns:
        Inteiro com o número de estudantes formados (egressos).
    
    Nota:
        Para usar este método, se o 'codigo_do_curso' não tiver sido informado pelo usuário, ele deve ser obtido previamente por `get_cursos_ativos` e recuperar o código do curso.
        Para usar este método, o 'periodo' deve ser informado pelo usuário, caso não seja fornecido, informe ao supervisor para buscar o **período mais recente** com o agente `Agente_Campus_Eureca`. 
    """
    params = {
        "curso": codigo_do_curso,
        "situacao-do-estudante": "EGRESSOS",
        "periodo-de-evasao-de": periodo,
        "periodo-de-evasao-ate": periodo
    }

    response = requests.get(f'{base_url}/estudantes', params=params)

    if response.status_code == 200:
        return len(json.loads(response.text))
    else:
        return [{"erro": "Não foi possível obter informação da UFCG."}]