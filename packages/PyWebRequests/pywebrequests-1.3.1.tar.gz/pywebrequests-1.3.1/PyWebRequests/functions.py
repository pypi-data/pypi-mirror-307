import requests
from lxml import etree
from bs4 import BeautifulSoup
#
#
#
#
def get_file(url: str, headers: dict = None, proxies: dict = None):
    return requests.get(url=url, headers=headers, proxies=proxies)
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
