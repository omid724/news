# In the name of God

import os
import re
import codecs
from time import sleep
from datetime import datetime

import requests
from bs4 import BeautifulSoup

from connection import send_news
from conf import desired_phrase, sites, should_send_to_chat

date_and_time = str(datetime.now())
date_exted = date_and_time[:4].replace("-", "_")
output_file_name = f"news_{date_exted}.txt"


def remove_slash(link):
    return link[:-1] if link[-1] == "/" else link


def remove_dot_in_first(link):
    return link[1:] if link[0] == "." else link


def find_domain(url):
    url = url.lower()
    # input shape: https://tarh.ir/golha/ ---> output shape: https://tarh.ir
    res_url = re.findall(r"^.+?\..+?/", url)
    res_url = res_url[0] if len(res_url) else url

    return res_url


def get_addresses(site):
    res = []
    try:
        d = requests.get(site, timeout=10)
    except Exception as e:
        print(f"error ocure while access to {site}, error: {str(e)}")
    else:
        soup = BeautifulSoup(d.text, "html.parser")
        res = soup.find_all("a")

    return res


def store_a_link_info_in_file(link_info, address):
    with codecs.open(output_file_name, "r+", "utf-8") as f:
        total_text = f.read()

        what_write = total_text + "\n" + address
        address = address[:-1] if address[-1] == "/" else address

        if address not in total_text:
            print(link_info)
            if should_send_to_chat:
                send_news(
                    "-" * 75
                    + "\n"
                    + link_info
                    + "\n"
                    + "-" * 75
                    + "\nAutomatic crawl and post by robot"
                )

            # Move the file pointer to the beginning of the file
            f.seek(0)

            f.write(what_write)

            # Truncate any remaining content after the new content (if any)
            f.truncate()


def make_link_info(desired_url, link_tag):
    address = link_tag.attrs["href"]
    address = address.strip()
    address = remove_dot_in_first(address)

    domain = remove_slash(find_domain(desired_url))

    if address[0:2] == "//":

        address = address[2:]

    elif address[0] == "/":

        address = domain + address

    link_text = link_tag.text.strip()

    link_info = link_text + "\n" + address + "\n" + "source: " + desired_url

    return link_info, address


def explore_a_site(desired_site):
    all_links_tags_in_it = get_addresses(desired_site)

    for link_tag in all_links_tags_in_it:
        exist = False
        for phrase in desired_phrase:
            if ((" " + phrase) in link_tag.text.strip()) or (
                link_tag.text.strip().startswith(phrase)
            ):
                exist = True
                break

        if exist:
            link_info, address = make_link_info(desired_site, link_tag)
            store_a_link_info_in_file(link_info, address)


if __name__ == "__main__":
    if not os.path.isfile(output_file_name):
        with open(output_file_name, "w", encoding="utf-8") as f:
            f.write("In the name of God\n\n")

    while True:
        os.system("cls")
        print("In the name of God\n\n\n")

        for site in sites:
            explore_a_site(site)

        sleep(1200)
