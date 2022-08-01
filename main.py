from config import pages_count
import exel_utils
import parsers.static_parse as sp
from exel_utils import get_data_fro_col, insert_data, FILEPATH
from config import *
from parsers.proxychanger import find_working_proxies
import parsers.dynamic_parse as dp

def main():
    pass
    # <-------STATICAL PARSING------>
    wb = exel_utils.workbook
    ws = wb.active
    pages = ['https://auto.ria.com/uk/legkovie/?page=' + str(i) for i in range(1, pages_count + 1)]
    # <---------------------------DATA INPUT PART-------------------------->
    # <----OLX---->
    # titles = sp.StaticItem("Titles", 'a', 'text', ('', ''), {'class': 'marginright5 link linkWithHash detailsLink'})
    # hrefs = sp.StaticItem("Hrefs", 'a', 'href', ('', ''), {'class': 'marginright5 link linkWithHash detailsLink'})
    # title_item = dp.DynamicItem("Titles", "h1", 'textContent', {'class': '_3Trjq aeJVe AeJ7R htldP'})
    # login_item = dp.DynamicItem('Login', 'input', '', {'id': 'userEmail'})
    # psswd_item = dp.DynamicItem('Password', 'input', '', {'id': 'userPass'})
    # login_form = dp.LoginItem(login_item, psswd_item, 'petrdobrev1994@gmail.com', 'oRWCc%#qSgxiI7Gs3%1jGM1c8z&%')
    # phone_button = dp.DynamicItem("Button", "button", '', {'class': 'css-65ydbw-BaseStyles'})
    # phone_item = dp.DynamicItem("Phones", 'a', 'textContent', {'class': 'css-v1ndtc'})
    # views = dp.DynamicItem('Views', 'span', 'textContent', {'class': 'css-1qvxqpo'})

    # <----AURO RIA---->
    titles = sp.StaticItem("Titles", 'a', 'title', ('', ''), {'class': 'address'})
    hrefs = sp.StaticItem("Hrefs", 'a', 'href', ('', ''), {'class': 'address'})
    prices = sp.StaticItem('Prices', 'span', 'text', ('', ''), {'data-currency': 'USD'})
    runs = sp.StaticItem('Runs', 'li', 'text', ('', " "), {'class': 'item-char js-race'})
    dates = sp.StaticItem('Dates', 'div', 'text', ('', ''), {'class': 'footer_ticket'})
    places = sp.StaticItem('Places', 'li', 'text', ('', ''), {'class': 'item-char view-location js-location'})

    phone_button = dp.DynamicItem("Button", 'a', '', {'class': 'size14 phone_show_link link-dotted mhide'})
    phone_item = dp.DynamicItem("Phones", 'div', 'textContent', {'class': 'popup-successful-call-desk size24 bold green mhide green'})

    static_results = {'Titles': [], 'Hrefs': [], 'Prices': [], 'Runs': [], 'Dates': [], 'Places': []}
    all_results = {'Titles': [], 'Hrefs': [], 'Prices': [], 'Runs': [], 'Dates': [], 'Places': [], 'Phones': []}
    names = list(all_results.keys())
    # <--------------FINDING WORKING PROXIES------------------>
    proxies = find_working_proxies(proxy_file, pages[0])
    while len(list(set(proxies))) < min_proxies_count:
        proxies.extend(find_working_proxies(proxy_file, pages[0]))
    # <-------------------PARSING PART------------------------>
    static_results = sp.parse_static(proxies, static_results, pages, [titles, hrefs, prices,runs, dates, places], all=1)
    print(f"\nStatic parsed items have a look like this: {static_results[0]}\n")
    dynamic_cells = dp.parse_dynamic(static_results, 1, None, proxies, [{phone_button: ['click', 0]},
                                                                                {phone_item: ['get', 0]}
                                                                                ])
    # <-------------------DATA INSERTING PART----------------->
    for cell in dynamic_cells:
        for name, values in all_results.items():
            all_results[name].append(cell[names.index(name)])

    insert_data(ws, 2, all_results)
    wb.save(FILEPATH)
    print("<----------SUCCESSFULLY FINISHED PARSING----------->")

    wb.close()
if __name__ == '__main__':
    main()
