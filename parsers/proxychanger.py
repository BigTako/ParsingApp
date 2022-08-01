import requests
import csv
import concurrent.futures
import config as conf


def get_proxies_from_file(filename):
    """Function to get proxy IP addresses from CSV file
        -> filename - name of csv file with proxies"""
    proxylist = []
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            if len(row)!=0:
                proxylist.append(row[0])
    return list(set(proxylist))


def connect_by_proxy(proxy:str, page:str, timeout):
    """Function to connect to page with given proxy IP address"""
    try:
        requests.get(page, headers=conf.HEADERS, proxies={'http': proxy, 'https': proxy}, timeout=timeout)
        print(f'[INFO] {proxy} successfully connected!')
        return proxy
    except Exception:
        pass


def find_working_proxies(filename: str, page: str):
    """Function of finding working proxy addresses by paralel sending requests.
        Returns list of working proxies"""
    working_proxies = []
    print("Started checking proxies...")
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = []
        ip_s = get_proxies_from_file(filename)
        for address in ip_s:
            futures.append(executor.submit(connect_by_proxy, proxy=address, page=page, timeout=conf.connect_timeout))
    for future in concurrent.futures.as_completed(futures):
        ip = future.result()
        if ip is not None:
            working_proxies.append(ip)
    return working_proxies









