import asyncio, sys
from langchain_core.messages import HumanMessage
from agents.build_agents import build

async def run(system, query, config):
    """
    Executa o sistema com uma query e retorna a resposta.
    """
    inputs = {"messages": [HumanMessage(content=query)]}
    async for chunk in system.astream(inputs, config, stream_mode="values"):
        chunk["messages"][-1].pretty_print()

async def main():
    """
    Iniciar a aplicação.
    """
    system = build()
    
    #print(system.get_graph().draw_mermaid())
    
    if len(sys.argv) < 2:
        print("Erro.")
    else:
        query = " ".join(sys.argv[1:])
        config = {"configurable": {"thread_id": "1"}}
        await run(system, query, config)

if __name__ == '__main__':
    asyncio.run(main())