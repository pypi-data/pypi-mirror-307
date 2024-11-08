import requests
from lxml import etree
from bs4 import BeautifulSoup
#
#
#
#
def get_json(url: str, headers: dict = None, proxies: dict = None):
    return requests.get(url=url, headers=headers, proxies=proxies).json()
#
#
#
#
def get_html(url: str, headers: dict = None, proxies: dict = None):
    return etree.HTML(
            str(
                    BeautifulSoup(requests.get(url=url, headers=headers, proxies=proxies).content, "html.parser")
            )
    )
#
#
#
#
def find_web_elements(etree_, xpath: str):
    return etree_.xpath(xpath)
#
#
#
#
def find_web_element(etree_, xpath: str):
    try:
        return find_web_elements(etree_, xpath)[0]
    except IndexError:
        return None
#
#
#
#
def get_random_user_agent():
    return find_web_element(
            get_html("https://user-agents.net/random", headers={"User-Agent": "Mozilla/5.0"}),
            "//ol/li/a"
    ).text
#
#
#
#
def get_free_proxies(protocol: str | list[str] = None):
    proxies = requests.get(
            url="https://raw.githubusercontent.com/proxifly/free-proxy-list/main/proxies/all/data.json",
            headers={"User-Agent": get_random_user_agent()}
    ).json()

    if protocol is None:
        return {proxy["protocol"]: proxy["proxy"] for proxy in proxies}
    else:
        if type(protocol) == list:
            return {
                proxy["protocol"]: proxy["proxy"] for proxy in filter(lambda proxy: proxy["protocol"] in protocol, proxies)
            }
        else:
            return {
                proxy["protocol"]: proxy["proxy"] for proxy in filter(lambda proxy: proxy["protocol"] == protocol, proxies)
            }
