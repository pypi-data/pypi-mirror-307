import requests
from PyWebRequests.functions import find_web_element, get_html
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
