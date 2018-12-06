import itertools

import argparse
import json
import os
import urllib.error
import urllib.request
from bs4 import BeautifulSoup


def get_soup(url):
    header = {'User-Agent':
                  "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36"}
    return BeautifulSoup(urllib.request.urlopen(urllib.request.Request(url, headers=header)), 'html.parser')


def scrape_google_image(query, max_num=1, name=None):
    if name is None:
        name = query
    save_directory = os.path.join("images", name)
    os.makedirs(save_directory, exist_ok=True)
    url_query = '+'.join(query.split())
    url = r"https://www.google.co.in/search?q=" + url_query + "&source=lnms&tbm=isch"
    soup = get_soup(url)

    print("Scraping for Images of", query)
    n_images = 0
    for element in itertools.takewhile(lambda _: n_images < max_num, soup.find_all("div", {"class": "rg_meta"})):
        link = json.loads(element.text)["ou"]
        extension = link.split(".")[-1]
        if extension in ["png", "jpeg", "jpg"]:
            try:
                save_path = os.path.join(save_directory, str(n_images + 1) + '.' + extension)
                urllib.request.urlretrieve(link, save_path)
                print("Images Downloaded:", n_images + 1)
                n_images += 1
            except urllib.error.HTTPError:
                pass
    return save_directory


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('keywords', nargs='+', help="Enter the keyword: ")
    parser.add_argument('--filename', nargs='?', help="Name of the file (default:keyword)")
    parser.add_argument('--max_num', nargs=1, default=10, help='Maximum number of images (default:10)')
    args = parser.parse_args()
    print('Images stored in:',
          scrape_google_image(query=' '.join(args.keywords), max_num=args.max_num, name=args.filename))
