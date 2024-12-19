from tools.other.web_search_tools import *
#from test_tools_eureca import *
from tools.eureca.backups.eureca_cc_tools import *
from tools.eureca.campus_tools import *
from tools.other.guia_tools import *
from tools.other.resolucao_tools import *
from tools.other.localizacao_tools import *
#from rag.guia.guia_vectordb import *
from rag.resolucao.resolucao_vectordb import *
from vectordb import Memory

# print(read_page("https://www.prac.ufcg.edu.br/ultimas-noticias"))

base_url = "https://eureca.sti.ufcg.edu.br/das/v2"
course = "14102100"
#print(get_cursos_ativos(base_url))
#print(get_campi(base_url))
print(get_periodo_mais_recente(base_url))

#mem = Memory(chunking_strategy={"mode": "sliding_window", "window_size": 14, "overlap": 10})
#save_vectordb(mem, create_sections("./rag/guia/guia.txt"), "./guia_db.pkl")
#print(type(get_guia_de_matriculas("quais são os pré-requisitos das disciplinas?")))

#mem = Memory(chunking_strategy={"mode": "sliding_window", "window_size": 14, "overlap": 10})
#save_vectordb(mem, create_sections("./rag/resolucao/resolucao.pdf"), "./resolucao_db.pkl")
#print(get_resolucao("quais os documentos necessários para realizar matrícula?"))

#print(read_localization_txt(""))