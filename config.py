pages_count = 100  # count of pages needed to be parsed

dynamic_delay = 10  # delay of waiting until element existence
connect_timeout = 3  # static page connection timeout
min_proxies_count = 7 # minimal count of proxies required to be successfully connected to
max_proxy_connections = 8  # max count of proxy to be connected to until it will be deleted from proxy list
max_trying_count = 10  # max count of connection trying,
parsing_pages_group =  10 # count of parsing pages in one group

proxy_file = 'proxylist.csv'
login_page = ''
browser_location = r'"C:\Program Files\Google\Chrome\Application\chrome.exe"'
HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:85.0) Gecko/20100101 Firefox/85.0',
               'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'}


