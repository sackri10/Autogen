from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.conditions import TextMentionTermination
from agents.Data_Analyzer_agent import getDataAnalyzerAgent
from agents.Code_executor_agent import getCodeExecutorAgent

def getDataAnalyzerTeam(docker,model_client):
    data_analyzer_agent = getDataAnalyzerAgent(model_client)
    code_executor_agent = getCodeExecutorAgent(docker)
    text_mention_termination = TextMentionTermination('STOP')

    team = RoundRobinGroupChat(
        participants=[data_analyzer_agent, code_executor_agent],
        termination_condition=text_mention_termination,
        max_turns=10,
    )

    return team