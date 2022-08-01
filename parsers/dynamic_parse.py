import selenium.common.exceptions
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from config import *
import time
from parsers.exceptions import *
from  parsers.proxychanger import find_working_proxies, concurrent
from webdriver_manager.chrome import ChromeDriverManager
import random

options = Options()
options.binary_location = browser_location


class DynamicItem:
    """Class of a dynamic parsing item. Was created especially for items, which aren't in initial HTML page
        but load with time, or requires an action to uncover it."""
    def __init__(self, name: str, tag: str, type: str, attributes: dict):
        self.name = name  # Name of item(name of column with data in xlsx file)
        self.type = type
        self.tag = tag.casefold()  # item HTML tag
        self.attributes = attributes  # item attributes


class LoginItem:
    """Class of a login items. Conteins """
    def __init__(self, login_item:DynamicItem, password_item:DynamicItem, login:str, password:str):
        self.login_item = login_item
        self.password_item = password_item
        self.login = login
        self.password = password


def attributes_to_xpath(item:DynamicItem):
    """Function to transform DynamicItem attributes(dict) to XPAHT"""
    result = f'//{item.tag}'
    for atr, value in item.attributes.items():
        result += f"[@{atr}='{value}']"
    return result


def get_text(driver:webdriver, dynamic_item:DynamicItem, all=0):
    """Function to parse info about needed dynamic items from HTML page
       -->driver - selenium.webdriver object (page must be opened before!)
       -->selection - content of attribute you want to select(textContent, href)
       -->dynamic_item - needed dynamic item(object)
       -->*all - parse all such elements in page(0), or not(1)
       """
    try:
        elem = 0
        if (all):  # if parse all items
            elem = WebDriverWait(driver, dynamic_delay).until(
                EC.presence_of_all_elements_located((By.XPATH, attributes_to_xpath(dynamic_item)))
            )
        else:
            elem = WebDriverWait(driver, dynamic_delay).until(
                EC.presence_of_element_located((By.XPATH, attributes_to_xpath(dynamic_item)))
            )
        result = []
        if not all:
            result = elem.get_attribute(dynamic_item.type)
        else:
            for e in elem:
                result.append(e.get_attribute(dynamic_item.type))
        return result
    except selenium.common.TimeoutException:
        return


def click_button(driver:webdriver, dynamic_button:DynamicItem):
    """Function of clicking a clickable object
        -->driver - selenium.webdriver object (page must be opened before!)
        -->dynamic_button - needed dynamic item(object)
    """
    try:
        driver.execute_script("arguments[0].click();", WebDriverWait(driver, dynamic_delay).until(
            EC.element_to_be_clickable((By.XPATH, attributes_to_xpath(dynamic_button)))))
        time.sleep(3)
        return 1
    except selenium.common.exceptions.TimeoutException:
        return 0


def paste_text(driver:webdriver, text:str, dynamic_item:DynamicItem, key=None):
    """Function of pasting some text into HTML page text field
        -->driver - selenium.webdriver object (page must be opened before!)
        -->text - text to be pasted
        -->dynamic_item - needed dynamic item(object)
        -->key* - what key will be pressed after pasting text
    """
    elem = WebDriverWait(driver, dynamic_delay).until(
        EC.presence_of_element_located((By.XPATH, attributes_to_xpath(dynamic_item)))
    )
    elem.send_keys(text)
    if key is not None:
        elem.send_keys(key)


def login_on_page(driver:webdriver, login: LoginItem , delay=1):
    """Function of filling login and password fields(simple login)
        -->driver - selenium.webdriver object (page must be opened before!)
        -->login - LoginItem with login form information and data
        -->delay* - delay between pasting text and pages load
    """
    try:
        paste_text(driver, login.login, login.login_item)
        time.sleep(delay)
        paste_text(driver, login.password, login.password_item, Keys.ENTER)
        time.sleep(delay + 2)
        return 1
    except Exception:
        return 0


def __dynamic_parse(data_tuples: list[tuple], results:list, login:LoginItem, page_indx:int,  proxies: dict[str:int],
                    ip_s:list[str], items:dict[DynamicItem:list[str, int]], indx=1):
    """Auxiliary function which does paralel parsing of given list of items from page
        (actions are taken in order of it's position in the list.
        Attributes:
              -> data tuples with already parsed data(including pages)
              ->results - list
              ->login - LoginItem with data to login on page
              ->proxies - list of working proxies
              ->items - list of dictionaries in format: {dynamic_item: [action, all]}
                *dynamic_item - needed item to parse
                *action - what action is required to do
                *all - should program parse all the data like dynamic_item on page or only one
              -> indx - recursive index
              -> ip_s - list of proxy IP addresses
        Returns nothing, only fills complete dictionary with results.
        If item of item is failed, function will reсall itself recursively until item will be parsed.
    """
    global dynamic_delay
    proxy = random.choice(ip_s)  # random proxy from list
    proxies[proxy] += 1
    current_data_cell = 0
    driver = 0
    try:
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--proxy-server=%s' % proxy)  # change user proxy
        # chrome_options.add_argument("--headless") # if you have no button to click
        driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)
        if login is not None:
            driver.get(login_page)
            print("Started logining in page")
            successful = login_on_page(driver, login)
            if not successful:
                raise Exception
            print("Successfully login in page")
        for data_cell in data_tuples:
            current_data_cell = data_cell
            print('Started parsing')
            page = data_cell[page_indx]
            driver.get(page)
            for item in items:  # type(item) - > dict ; {dynamic_item: [action, all]}
                dynamic_item = list(item.keys())[0]
                info = list(item.values())[0]  # [action, all]
                selection = info[0]  # action
                all = info[1]
                if selection == 'get':
                    print(f'Started parsing {page}')
                    data = get_text(driver, dynamic_item, all)
                    if data is None:
                        raise NoSuchElementExeption(dynamic_item.name, dynamic_item.tag, dynamic_item.attributes)
                    else:
                        results.append(list(data_cell + (data,)))
                    print(f'Successfully parsed page {page}')
                if selection == 'click':
                    print(f'Clicking button in page {page}')
                    successful = click_button(driver, dynamic_item)
                    if not successful:
                        raise NoSuchElementExeption(dynamic_item.name, dynamic_item.tag, dynamic_item.attributes)
                    print(f'Successfully clicked button on page {page}')
        dynamic_delay-=1
        return 1
    except Exception as ex:
        dynamic_delay+=1
        if proxies[proxy] == max_proxy_connections:
            del proxies[proxy]
            ip_s = list(filter((proxy).__ne__, ip_s))

        print(f"Session {proxy} | Failed to connect! | Reloaded {indx} times.")
        if indx == max_trying_count:
            print("Ad-s isn't active or something else went wrong!")
            results.append(list(current_data_cell + (" ",)))
            data_tuples.remove(current_data_cell)
            indx = 0
        print(ex)
        driver.close()
        return __dynamic_parse(data_tuples, results, login, page_indx, proxies, ip_s, items, indx+1)


def parse_dynamic(data:list[tuple], page_indx:int, login, ip_s:list[str], items: list[dict[list[str, int]:DynamicItem]]):
    """ Main function of dynamic parsing. Directly uses to parse dynamic items.
        -> data tuples with already parsed data(including pages)
        -> page_indx - index of url to page in tuple
        ->proxy_file -> file with proxy IP addresses
        ->items - list of dictionaries in format: {dynamic_item: [action, all]}
                *dynamic_item - needed item to parse
                *action - what action is required to do
                *all - should program parse all the data like dynamic_item on page or only one
        Returns dictionary with results of parsing.
    """
    results = []
    proxies = {ip: 0 for ip in ip_s}
    print('<-----STARTED DYNAMIC PARSING----->')
    futures = []
    pages_index = 0
    if parsing_pages_group > len(data):
        print("Count of pages in parsing group lower then given data len")
        return []
    with concurrent.futures.ThreadPoolExecutor() as executor:
        while (pages_index < len(data)):
            if pages_index + parsing_pages_group < len(data):
                futures.append(executor.submit(
                    __dynamic_parse,
                    data_tuples=data[pages_index:pages_index+parsing_pages_group],
                    results=results,
                    login=login,
                    page_indx=page_indx,
                    proxies=proxies,
                    ip_s=ip_s,
                    items=items
                ))
            else:
                futures.append(executor.submit(
                    __dynamic_parse,
                    data_tuples=data[pages_index:pages_index + parsing_pages_group],
                    results=results,
                    login=login,
                    page_indx=page_indx,
                    proxies=proxies,
                    ip_s=ip_s,
                    items=items
                ))
            pages_index += parsing_pages_group
    return results



