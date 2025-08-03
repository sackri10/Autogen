import asyncio
from teams.analyzer_gpt import getDataAnalyzerTeam
from models.openai_model_client import get_model_client
from config.docker_util import get_docker_code_executor, start_docker_container, stop_docker_container
from autogen_agentchat.messages import TextMessage

async def main():

    openai_model_client = get_model_client()
    docker =get_docker_code_executor()

    team =getDataAnalyzerTeam(docker, openai_model_client)

    try:
        task = 'Can you give me a graph of types of flowers in my data iris.csv?' 
        
        await start_docker_container(docker)

        async for message in team.run_stream(task =task):
            print(message
            )
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        await stop_docker_container(docker)
        print("Docker container stopped.")

if __name__ == "__main__":

    asyncio.run(main())
    print("Main function completed.")   