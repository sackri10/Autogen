import asyncio
from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_core.tools import FunctionTool
from autogen_agentchat.ui import Console
import os
from autogen_core.tools import FunctionTool
from dotenv import load_dotenv

from langchain_community.utilities import GoogleSerperAPIWrapper

from autogen_ext.tools.http import HttpTool
from autogen_agentchat.conditions import TextMentionTermination,MaxMessageTermination,ExternalTermination

# Load environment variables
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("Please set the OPENAI_API_KEY environment variable.")

model_client=OpenAIChatCompletionClient(model='gpt-4o',api_key=api_key)

from autogen_agentchat.agents import AssistantAgent

first_agent = AssistantAgent(
    name="First_Agent",
    model_client=model_client,
    system_message="You are the first agent in a round-robin setup. Your task is to process the input which contains a number, increment that number by 1 and pass it to the next agent.",
    description="This agent processes the input and passes it to the next agent in the round-robin setup.", 
)

second_agent = AssistantAgent(
    name="Second_Agent",
    model_client=model_client,
    system_message="You are the second agent in a round-robin setup. Your task is to process the input which contains a number, multiply that number by 2 and pass it to the next agent.", 
    description="This agent processes the input and passes it to the next agent in the round-robin setup.",
)
third_agent = AssistantAgent(
    name="Third_Agent",
    model_client=model_client,
    system_message="You are the third agent in a round-robin setup. Your task is to process the input which contains a number, subtract 3 from that number and return the final result.",
    description="This agent processes the input and returns the final result.",
)

# Define the round-robin function
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.messages import TextMessage

team=RoundRobinGroupChat(
    participants=[first_agent, second_agent, third_agent],
    max_turns=3
)

async def run_team():
    """Run the round-robin team with a sample input."""
    input_number = 510
    print(f"Starting with input: {input_number}")
    
    # Start the round-robin process
    result = await team.run(task=TextMessage(content=str(input_number),source="user"))  # Use TextMessage to pass the input
    
    # Print the final result from the last agent
    print(f"Final result: {result.messages[-1].content}")


teamWithMaxTurnAs6 =RoundRobinGroupChat(
    participants=[first_agent, second_agent, third_agent],
    max_turns=6
)

async def run_team_MaxTurn6():
    """Run the round-robin team with a sample input."""
    input_number = 510
    print(f"Starting with input: {input_number}")
    
    # Start the round-robin process
    result = await teamWithMaxTurnAs6.run(task=TextMessage(content=str(input_number),source="user"))  # Use TextMessage to pass the input
    
    # Print the final result from the last agent
    print(f"Final result: {result.messages[-1].content}")

async def run_team_WithTextTerminationCondition():
   

    first_agent_terminate = AssistantAgent(
        name="First_Agent",
        model_client=model_client,
        system_message="You are the first agent in a round-robin setup. Your task is to process the input which contains a number, increment that number by 1 and pass it to the next agent. Before process if you see the number is greater than 1000, then terminate the round-robin process and return 'TERMINATE'.",
        description="This agent processes the input and passes it to the next agent in the round-robin setup.", 
    )

    second_agent_terminate = AssistantAgent(
        name="Second_Agent",
        model_client=model_client,
        system_message="You are the second agent in a round-robin setup. Your task is to process the input which contains a number, multiply that number by 2 and pass it to the next agent. Before process if you see the number is greater than 1000, then terminate the round-robin process and return 'TERMINATE'.", 
        description="This agent processes the input and passes it to the next agent in the round-robin setup.",
    )
    third_agent_terminate = AssistantAgent(
        name="Third_Agent",
        model_client=model_client,
        system_message="You are the third agent in a round-robin setup. Your task is to process the input which contains a number, subtract 3 from that number and return the final result. Before process if you see the number is greater than 1000, then terminate the round-robin process and return 'TERMINATE'.",
        description="This agent processes the input and returns the final result.",
    )
    termination_condition = TextMentionTermination(text="TERMINATE")

    teamWithTerminationCondition =RoundRobinGroupChat(
    participants=[first_agent_terminate, second_agent_terminate, third_agent_terminate],
    max_turns=12,
    termination_condition=termination_condition
    )
    """Run the round-robin team with a sample input."""
    input_number = 300
    print(f"Starting with input: {input_number}")
    
    # Start the round-robin process
    result = await teamWithTerminationCondition.run(task=TextMessage(content=str(input_number),source="user"))  # Use TextMessage to pass the input
    # Print all the messages from agents
    for each_agent_message in result.messages:
        print(f"{each_agent_message.source} : {each_agent_message.content}")

async def run_team_WithTextAndMessageTerminationCondition():
   

    first_agent_terminate = AssistantAgent(
        name="First_Agent",
        model_client=model_client,
        system_message="You are the first agent in a round-robin setup. Your task is to process the input which contains a number, increment that number by 1 and pass it to the next agent. Before process if you see the number is greater than 1000, then terminate the round-robin process and return 'TERMINATE'.",
        description="This agent processes the input and passes it to the next agent in the round-robin setup.", 
    )

    second_agent_terminate = AssistantAgent(
        name="Second_Agent",
        model_client=model_client,
        system_message="You are the second agent in a round-robin setup. Your task is to process the input which contains a number, multiply that number by 2 and pass it to the next agent. Before process if you see the number is greater than 1000, then terminate the round-robin process and return 'TERMINATE'.", 
        description="This agent processes the input and passes it to the next agent in the round-robin setup.",
    )
    third_agent_terminate = AssistantAgent(
        name="Third_Agent",
        model_client=model_client,
        system_message="You are the third agent in a round-robin setup. Your task is to process the input which contains a number, subtract 3 from that number and return the final result. Before process if you see the number is greater than 1000, then terminate the round-robin process and return 'TERMINATE'.",
        description="This agent processes the input and returns the final result.",
    )
    termination_condition = TextMentionTermination(text="TERMINATE") | MaxMessageTermination(max_messages=5)

    teamWithTerminationCondition =RoundRobinGroupChat(
    participants=[first_agent_terminate, second_agent_terminate, third_agent_terminate],
    max_turns=12,
    termination_condition=termination_condition
    )
    """Run the round-robin team with a sample input."""
    input_number = 50
    print(f"Starting with input: {input_number}")
    
    # Start the round-robin process
    result = await teamWithTerminationCondition.run(task=TextMessage(content=str(input_number),source="user"))  # Use TextMessage to pass the input
    # Print all the messages from agents
    for each_agent_message in result.messages:
        print(f"{each_agent_message.source} : {each_agent_message.content}")
    #reset a team
    teamWithTerminationCondition.reset()

async def run_team_WithExternalTerminationCondition():
   

    first_agent_terminate = AssistantAgent(
        name="First_Agent",
        model_client=model_client,
        system_message="You are the first agent in a round-robin setup. Your task is to process the input which contains a number, increment that number by 1 and pass it to the next agent. Before process if you see the number is greater than 1000, then terminate the round-robin process and return 'TERMINATE'.",
        description="This agent processes the input and passes it to the next agent in the round-robin setup.", 
    )

    second_agent_terminate = AssistantAgent(
        name="Second_Agent",
        model_client=model_client,
        system_message="You are the second agent in a round-robin setup. Your task is to process the input which contains a number, multiply that number by 2 and pass it to the next agent. Before process if you see the number is greater than 1000, then terminate the round-robin process and return 'TERMINATE'.", 
        description="This agent processes the input and passes it to the next agent in the round-robin setup.",
    )
    third_agent_terminate = AssistantAgent(
        name="Third_Agent",
        model_client=model_client,
        system_message="You are the third agent in a round-robin setup. Your task is to process the input which contains a number, subtract 3 from that number and return the final result. Before process if you see the number is greater than 1000, then terminate the round-robin process and return 'TERMINATE'.",
        description="This agent processes the input and returns the final result.",
    )
    ext_Termination =ExternalTermination() 
    termination_condition = ext_Termination | TextMentionTermination(text="TERMINATE") | MaxMessageTermination(max_messages=5)

    teamWithTerminationCondition =RoundRobinGroupChat(
    participants=[first_agent_terminate, second_agent_terminate, third_agent_terminate],
    max_turns=12,
    termination_condition=termination_condition
    )
    """Run the round-robin team with a sample input."""
    input_number = 50
    print(f"Starting with input: {input_number}")
    
    # Start the round-robin process
    result = asyncio.create_task(Console(teamWithTerminationCondition.run_stream(task=TextMessage(content=str(input_number),source="user"))))  # Use TextMessage to pass the input

    # Wait for some time.
    await asyncio.sleep(0.1)

    # Check if the termination condition is met
    ext_Termination.set()
    # Print all the messages from agents
    await result
    
    await (Console(teamWithTerminationCondition.run_stream()))



if __name__ == "__main__":
    #asyncio.run(run_team())
    #asyncio.run(run_team_MaxTurn6())
    #asyncio.run(run_team_WithTextTerminationCondition())
    #asyncio.run(run_team_WithTextAndMessageTerminationCondition())
    asyncio.run(run_team_WithExternalTerminationCondition())
    


