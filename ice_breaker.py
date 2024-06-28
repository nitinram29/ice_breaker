from langchain.prompts.prompt import PromptTemplate
from langchain_openai import ChatOpenAI, chat_models
from dotenv import load_dotenv
from third_parties.linkedin_scraper import linkedin_scraper

if __name__ == "__main__":

    load_dotenv()

    summary_template = """
        given a linkedin profile information {information}, give following info from that:
        1) short summary
        2) two interesting fact about them
    """

    summary_template_prompt = PromptTemplate(
        input_variables=["information"], template = summary_template)

    llm = chat_models.AzureChatOpenAI(
        model = "gpt-4-32k",
        temperature = 0,
        azure_endpoint = "https://oceanfreightailabs.openai.azure.com/",
        azure_deployment = "ocean_gpt4_32k",
    )

    chain = summary_template_prompt | llm

    linkedin_scraped_data = linkedin_scraper("http://linkedin.com/in/nitin-ram-a9b1a91b2/", mock=True)

    res = chain.invoke(input={"information":linkedin_scraped_data})

    print(res)