#!/usr/bin/python3
# -*- coding: utf-8 -*-

import itertools
import argparse
import json
import logging
import os
import urllib.request
from urllib.error import HTTPError, URLError
from bs4 import BeautifulSoup

logging.getLogger().setLevel(11)

def get_soup(url):
    header = {'User-Agent':
                  "Mozilla/5.0 (Linux; U; Android 4.4.2; en-us; SCH-I535 Build/KOT49H)"}
    return BeautifulSoup(urllib.request.urlopen(urllib.request.Request(url, headers=header)), 'lxml')


def scrape_google_image_on_demand(query, search_engine='www.google.co.in'):
    try:
        url_query = '+'.join(query.split())
        url = r"https://%s/search?q=%s&source=lnms&tbm=isch" % (search_engine, url_query)
        logging.log(11,"Querying for: %s",url)
        soup = get_soup(url)
        n_images = 0
        for element in soup.find_all("div", {"class": "rg_meta"}):
            link = json.loads(element.text)["ou"]
            extension = link.split(".")[-1]
            if extension in ["png", "jpeg", "jpg"]:
                with urllib.request.urlopen(link) as request:
                    image = request.read()
                logging.log(11,"Images downloaded: %s",link)
                n_images += 1
                yield image
    except (HTTPError, URLError):
        return

def scrape_google_image(query, max_num=1, search_engine='www.google.co.in', name=None,):
    if name is None:
        name = query
    save_directory = os.path.join("images", name)
    os.makedirs(save_directory, exist_ok=True)
    for n_images,image in zip(range(max_num),scrape_google_image_on_demand(query=query, search_engine=search_engine)):
        save_path = os.path.join(save_directory, str(n_images + 1) + '.' + '.png')
        with open(save_path,'wb') as image_file:
            image_file.write(image)
    return save_directory


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Scraper for images related to query')
    parser.add_argument('keywords', nargs='+', help="Keywords")
    parser.add_argument('--search-engine', nargs=1, default='www.google.co.in',
                        help='search engine url (default:www.google.co.in)')
    parser.add_argument('--filename', nargs='?', help="Name of the file (default:keyword)")
    parser.add_argument('--max_num', nargs='?', default=3,type=int, help='Maximum number of images (default:3)')
    args = parser.parse_args()
    print('Images stored in:',
          scrape_google_image(query=' '.join(args.keywords), max_num=args.max_num, name=args.filename))
