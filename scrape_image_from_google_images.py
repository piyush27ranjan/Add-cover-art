import itertools

import argparse
import json
import logging
import os
import urllib.request
from bs4 import BeautifulSoup


def get_soup(url):
    header = {'User-Agent':
                  "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36"}
    return BeautifulSoup(urllib.request.urlopen(urllib.request.Request(url, headers=header)), 'html.parser')


def scrape_google_image_on_demand(query, max_num=1, search_engine='www.google.co.in'):
    url_query = '+'.join(query.split())
    url = r"https://%s/search?q=%s&source=lnms&tbm=isch" % (search_engine, url_query)
    logging.debug("Scraping for query: %s", query)
    soup = get_soup(url)
    n_images = 0
    for element in itertools.takewhile(lambda _: n_images < max_num, soup.find_all("div", {"class": "rg_meta"},limit=max_num)):
        link = json.loads(element.text)["ou"]
        extension = link.split(".")[-1]
        if extension in ["png", "jpeg", "jpg"]:
            with urllib.request.urlopen(link) as request:
                image = request.read()
            logging.debug("Images downloaded: %s", n_images + 1)
            n_images += 1
            yield image
    if n_images < 1:
        raise ValueError("No images downloaded")

def scrape_google_image(query, max_num=1, search_engine='www.google.co.in', name=None,):
    if name is None:
        name = query
    save_directory = os.path.join("images", name)
    os.makedirs(save_directory, exist_ok=True)
    for n_images,image in enumerate(scrape_google_image_on_demand(query=query, max_num=max_num, search_engine=search_engine)):
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
    parser.add_argument('--max_num', nargs=1, default=10, help='Maximum number of images (default:10)')
    args = parser.parse_args()
    print('Images stored in:',
          scrape_google_image(query=' '.join(args.keywords), max_num=args.max_num, name=args.filename))
