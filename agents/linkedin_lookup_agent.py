import os
from dotenv import load_dotenv
from langchain_openai import chat_models
from langchain.agents import create_react_agent, AgentExecutor
from langchain.prompts.prompt import PromptTemplate
from langchain_core.tools import Tool
from langchain import hub
from tools.tools import get_profile_url_tavily


load_dotenv()
def lookup(name: str, company_name:str, mock: bool= False) -> str:
    if mock:
        if name.lower() == "nitin ram":
            return "https://in.linkedin.com/in/nitin-ram-a9b1a91b2"
        if name.lower() == "tanisha barman":
            return "https://in.linkedin.com/in/tanisha-barman-7b12471b8"
        return "{'data': 'No data found'}"

    # creating LLM connection
    llm = chat_models.AzureChatOpenAI(
        model="gpt-4-32k",
        temperature=0,
        azure_endpoint="https://oceanfreightailabs.openai.azure.com/",
        azure_deployment="ocean_gpt4_32k",
    )

    # creating str prompt
    template = """Given a full name {name_of_profile} and wokring in {company_name}, I want you to get it me a link to their linkedin profile page.
                    your answer should contains only a URL"""

    # creating prompt and specifing the input variables in that templates
    template_prompt = PromptTemplate(
        input_variables=["name_of_profile","company_name"], template=template)

    # creating tools which our LLM will use to some work
    tools_for_agent = [
        Tool(
            name= "Crawl Google 4 linkedin page URL",
            func=get_profile_url_tavily,
            description="useful for when you need get the linkedin page URL"
        )
    ]

    # creating reAct prompt
    react_prompt = hub.pull("hwchase17/react")

    # creating agent
    agent = create_react_agent(llm=llm, tools=tools_for_agent, prompt=react_prompt)

    # creating agent executor
    agent_executor = AgentExecutor(agent=agent, tools=tools_for_agent, verbose=True)

    result = agent_executor.invoke(
        input={"input": template_prompt.format_prompt(name_of_profile=name, company_name=company_name)}
    )

    linkedin_profile_url = result["output"]
    return linkedin_profile_url

