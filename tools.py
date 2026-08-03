from langchain.tools import tool
from tavily import TavilyClient
from dotenv import load_dotenv
import os
import requests
from rich import print
from bs4 import BeautifulSoup
load_dotenv()

tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))


@tool
def web_search(query:str) -> str:
    """Search the web for recent and reliable information on a topic, Returns Titles, URL, Snippets"""
    result = tavily.search(
        query=query,
        max_results=5,
    )

    out = []

    for r in result["results"]:
        out.append(
            f"title: {r["title"]} \nUrl: {r["url"]} \nSnippet: {r["content"][:300]}\n"
        )
    return("\n-------\n".join(out))

# print(web_search.invoke("any weather news from pune ?"))

@tool
def scrape_url(url:str) -> str :
    """Scrape and return clean text content from s given URL for deeper reading."""

    print("----> url", url)
    try:
        resp = requests.get(url, timeout=8, headers={"User-Agent":"Mozilla/5.0"})
        # print("resp", resp)
        soup = BeautifulSoup(resp.text, "html.parser")
        # print("soup", soup)
        for tag in soup(["script", "style", "nav", "footer"]):
            tag.decompose()
        return soup.get_text(separator=" ", strip=True)[:3000]
    except Exception as e:
        return f"Could not scope URL: {str(e)}"

