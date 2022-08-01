import requests
from bs4 import BeautifulSoup
import config as conf
from parsers.proxychanger import concurrent, find_working_proxies
from parsers.exceptions import *
import random


class StaticItem:
    """Class of statical page item(that loads just with page and finds in source HTML code"""
    def __init__(self, name, tag, get_item, addition:tuple, fields):
        self.name = name  # name of item(name of column with data)
        self.tag = tag.casefold()  # HTML tag of item
        self.fields = fields  # a dictionary with HTML attributes(class, id...)
        self.addition = addition  # if item type str(f.e. href) what to add in the beginning
        self.get_item = get_item.casefold()  # content of attribute you want to get(text, href...)


def get_content(html, static_item:StaticItem, all=1):
    """Function of finding needed info about StaticItem in HTML code of page(c.b. text, href...)
        Attribute:
        -> html - HTML code of page
        -> static_item - StaticItem object
    """
    things = []
    soup = BeautifulSoup(html, "html.parser")
    if all:
        items = soup.find_all(static_item.tag, attrs=static_item.fields)  # finds all items with info like in static_block
        for item in items:
            if len(static_item.get_item) == 0 or static_item.get_item == 'text':  # if you want to get text of item
                things.append(static_item.addition[0] + item.text + static_item.addition[1])
            else:  # other item
                things.append(static_item.addition[0] + item.get(static_item.get_item) + static_item.addition[1])
    else:
        item = soup.find(static_item.tag, attrs=static_item.fields)
        if len(static_item.get_item) == 0 or static_item.get_item == 'text':  # if you want to get text of item
            things.append(static_item.addition[0] + item.text + static_item.addition[1])
        else:  # other item
            things.append(static_item.addition[0] + item.get(static_item.get_item) + static_item.addition[1])
    return things


def get_static_page_data(proxies: list[str], results:dict, page:str, items:list[StaticItem], all):
    """Auxiliary function which does paralel parsing of given list of items from page
            (actions are taken in order of it's position in the list).
            Attributes:
                  -> page - url to page with data
                  ->results - dictionary where parsing results will be stored ("Name of item": [])
                  ->proxies - list of working proxies
                  ->items - list of static items
            Returns nothing, only fills complete dictionary with results.
            If item of item is failed, function will reсall itself recursively until item will be parsed.
        """
    proxy = random.choice(proxies)
    try:
        html = requests.get(page, headers=conf.HEADERS, proxies={'http': proxy, 'https': proxy},
                            timeout=conf.connect_timeout)
        if html.status_code == 200:
            print(f'[INFO]https://{proxy} connected! | Page {page}')
            for item in items:
                data = get_content(html.text, item, all)
                if len(data) == 0:
                    raise NoSuchElementExeption(item.name, item.tag, item.fields)
                results[item.name].extend(data)
            print(f'[INFO] {proxy} parsed successfully! | Page {page}')
        else:
            raise Exception
    except NoSuchElementExeption as ex:
        print("[ERROR] " + str(ex))
        return {}
    except Exception:
        print(f"Page {page} | {proxy} | failed to connect!")
        return get_static_page_data(proxies, results,page, items, all)


def parse_static(proxies:list[str], results: dict, pages:list[str], items:list[StaticItem], all=1):
    """ Main function of static parsing. Directly uses to parse static items.
            ->pages -> list of pages required to parse
            -> results ->
            ->filename -> file with proxy IP addresses
            ->items - list of static items
        Returns dictionary with results of parsing.
        """
    print('<-----STARTED STATIC PARSING----->')
    futures = []
    print(proxies)
    with concurrent.futures.ThreadPoolExecutor() as executor:
        for page in pages:
            futures.append(executor.submit(get_static_page_data,
                                               proxies=proxies,
                                               results=results,
                                               page=page,
                                               items=items,
                                               all=all))
    return list(zip(*(results.values())))
