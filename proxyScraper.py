import os
import threading
import asyncio
import argparse
from pathlib import Path
import shutil

import requests
from bs4 import BeautifulSoup

default_output_directory = 'output'
default_output_file_name = default_output_directory + '/' + 'proxy_list'


def proxyScraper(website, proxy_type, proxy_timeout='1000', proxy_country='all', proxy_ssl='all', proxy_anonymity='all'):

    output_file_name = default_output_file_name + '_' + proxy_type + '.txt'

    if (website == 'proxyscrape'):
        scraper_for_proxyscrape(proxy_type, proxy_timeout, proxy_country,
                                proxy_ssl, proxy_anonymity, output_file_name)

    elif (website == 'proxy-list'):
        scraper_for_proxy_list(proxy_type, proxy_country,
                               proxy_anonymity, output_file_name)

    elif (website == 'free-proxy-list'):
        url = 'https://free-proxy-list.net'

        scrape_proxies_from_url(url, output_file_name)

    elif (website == 'sslproxies'):
        url = 'https://sslproxies.org'

        scrape_proxies_from_url(url, output_file_name)

    elif (website == 'us-proxy'):
        url = 'https://us-proxy.org'

        scrape_proxies_from_url(url, output_file_name)

    elif (website == 'socks-proxy'):
        url = 'https://socks-proxy.net'

        scrape_proxies_from_url(url, output_file_name)


def scraper_for_proxyscrape(proxy_type, proxy_timeout, proxy_country, proxy_ssl, proxy_anonymity, output_file_name):
    url = "https://api.proxyscrape.com/v2/?request=getproxies" + \
        "&protocol=" + proxy_type + \
        "&timeout=" + proxy_timeout + \
        "&country=" + proxy_country + \
        "&ssl=" + proxy_ssl + \
        "&anonymity=" + proxy_anonymity

    proxy_list = requests.get(url).text

    with open(output_file_name, "a") as file:

        file.write(proxy_list)


def scraper_for_proxy_list(proxy_type, proxy_country, proxy_anonymity, output_file_name):
    url = "https://www.proxy-list.download/api/v1/get" + '?type=' + proxy_type

    if (proxy_anonymity != 'all'):
        url += '&anon=' + proxy_anonymity

    if (proxy_country != 'all'):
        url += '$country=' + proxy_country

    proxy_list = requests.get(url).text

    # print_if_verbose(url + ' scraped successfully')

    with open(output_file_name, "a") as file:
        file.write(proxy_list)


def scrape_proxies_from_url(url, output_file_name):
    raw_html = requests.get(url).text

    # print_if_verbose(url + ' scraped successfully')

    parsed_html = parse_html(raw_html)

    html_table = table = parsed_html.find(
        'table', attrs={'id': 'proxylisttable'})

    extracted_proxy_list = scrape_proxies_from_html_table(html_table)

    proxy_list = set()

    proxy_list.update(extracted_proxy_list)

    with open(output_file_name, "a") as txt_file:

        for line in proxy_list:

            txt_file.write("".join(line) + "\n")


def parse_html(raw_html):
    parsed_html = BeautifulSoup(raw_html, "html.parser")

    return parsed_html


def scrape_proxies_from_html_table(table):
    proxies = set()

    table_rows = table.findAll('tr')

    for row in table_rows:

        count = 0
        proxy = ""

        table_cells = row.findAll('td')

        for cell in table_cells:

            if count == 1:
                proxy += ":" + cell.text.replace('&nbsp;', '')

                proxies.add(proxy)
                break

            proxy += cell.text.replace('&nbsp;', '')

            count += 1

    return proxies


# def print_if_verbose(text):
    # if args.verbose:
    #     print(text)


def remove_and_create_output_dir(dir_path):

    if (os.path.exists(dir_path)):
        shutil.rmtree(dir_path)

    os.mkdir(dir_path)


if __name__ == "__main__":

    # TODO: deduplicate

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-p", "--proxy", help="Proxy type: http ,https, socks, socks4, socks5")

    parser.add_argument("-v", "--verbose",
                        help="Increase output verbosity", action="store_true")

    args = parser.parse_args()
    proxy_type = args.proxy

    remove_and_create_output_dir(default_output_directory)

    # HTTP
    threading.Thread(target=proxyScraper, args=(
        'proxyscrape', 'http')).start()

    threading.Thread(target=proxyScraper, args=(
        'proxy-list', 'http')).start()

    threading.Thread(target=proxyScraper, args=(
        'us-proxy', 'http')).start()

    threading.Thread(target=proxyScraper, args=(
        'free-proxy-list', 'http')).start()

    # HTTPS
    threading.Thread(target=proxyScraper, args=(
        'proxyscrape', 'https')).start()

    threading.Thread(target=proxyScraper, args=(
        'proxy-list', 'https')).start()

    threading.Thread(target=proxyScraper, args=(
        'sslproxies', 'https')).start()

    # SOCKS4
    threading.Thread(target=proxyScraper, args=(
        'proxyscrape', 'socks4')).start()

    threading.Thread(target=proxyScraper, args=(
        'proxy-list', 'socks4')).start()

    threading.Thread(target=proxyScraper, args=(
        'socks-proxy', 'socks4')).start()

    # SOCKS5
    threading.Thread(target=proxyScraper, args=(
        'proxyscrape', 'socks5')).start()

    threading.Thread(target=proxyScraper, args=(
        'proxy-list', 'socks5')).start()
