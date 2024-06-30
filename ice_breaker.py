from typing import Tuple

from langchain.prompts.prompt import PromptTemplate
from langchain_openai import chat_models
from dotenv import load_dotenv
from agents.linkedin_lookup_agent import lookup
from output_parsers.output_parser import summary_parser, Summary
from third_parties.linkedin_scraper import linkedin_scraper

# When need to test end to end with TavilySearchResults and nubela, make mock as False in both the function
def ice_breaker_with(name: str, company_name: str) -> Tuple[Summary, str]:

    linkedin_url = lookup(name, company_name, mock=True)
    linkedin_scraped_data = linkedin_scraper(linkedin_url, mock=True)
    print(linkedin_scraped_data)

    llm = chat_models.AzureChatOpenAI(
        model="gpt-4-32k",
        temperature=0,
        azure_endpoint="https://oceanfreightailabs.openai.azure.com/",
        azure_deployment="ocean_gpt4_32k",
    )

    summary_template = """
        given a linkedin profile information {information}, give following info from that:
        1) short summary
        2) two interesting fact about them
        
        \n {format_instructions}
    """

    summary_template_prompt = PromptTemplate(
        input_variables=["information"], template = summary_template, partial_variables={"format_instructions":summary_parser.get_format_instructions()})


    chain = summary_template_prompt | llm | summary_parser

    res:Summary = chain.invoke(input={"information":linkedin_scraped_data})

    return res, linkedin_scraped_data.get("profile_pic_url")


# if __name__ == "__main__":
#     load_dotenv()
#     print(ice_breaker_with("NITIN RAM", "Kearney"))