import asyncio, sys
from langchain_core.messages import AIMessage, HumanMessage
from agents import build

async def run(system, query, config):
    """
    Executa o sistema com uma query e retorna a resposta.
    """
    inputs = {"messages": [HumanMessage(content=query)]}
    async for chunk in system.astream(inputs, config, stream_mode="values"):
        chunk["messages"][-1].pretty_print()

#query = "Quais são os comunicados oficiais mais recentes?"
#response = asyncio.run(run(query))
#print("Resposta do sistema:", response)

async def main():
    """Main entry point for the application."""
    system = build()
    
    # Uncomment to print the graph
    #print(system.get_graph().draw_mermaid())
    
    if len(sys.argv) < 2:
        print("Deu ruim!")
    else:
        query = " ".join(sys.argv[1:])
        # Initialize memory config for single query if needed
        config = {"configurable": {"thread_id": "1"}}
        await run(system, query, config)

if __name__ == '__main__':
    asyncio.run(main())