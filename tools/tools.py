from langchain_community.tools.tavily_search import TavilySearchResults


def get_profile_url_tavily(name: str, company_name: str):
    serach = TavilySearchResults()
    res = serach.run(f"name is {name}, company name is {company_name}")
    print(res[0]["url"])
    return res[0]["url"]
