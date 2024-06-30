import os
from dotenv import load_dotenv
import requests

load_dotenv()
def linkedin_scraper(linkedin_url, mock: bool = False):

    global response
    if mock:
        if linkedin_url.lower() == "https://in.linkedin.com/in/nitin-ram-a9b1a91b2":
            response = (requests.get(os.getenv("GIST_URL_NITIN")))
        if linkedin_url.lower() == "https://in.linkedin.com/in/tanisha-barman-7b12471b8":
            response = (requests.get(os.getenv("GIST_URL_TANISHA")))
    else:
        api_key = os.getenv("PROXYCURL_API_KEY")
        headers = {'Authorization': 'Bearer ' + api_key}
        api_endpoint = 'https://nubela.co/proxycurl/api/v2/linkedin'
        params = {
            'linkedin_profile_url': linkedin_url,
        }
        response = requests.get(api_endpoint,
                            params=params,
                            headers=headers)
    data = response.json()
    data = {
        k: v
        for k, v in data.items()
        if v not in [None, "", [], " "]
        and k not in ["people_also_viewed", "certifications"]
    }
    if data.get("groups"):
        for group_dict in data.get("groups"):
            group_dict.pop("profile_pic_url")
    return data


