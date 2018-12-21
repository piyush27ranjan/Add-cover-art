"""
Add Cover Art:
This application will find the .mp3 files in your computer.
Then it will automatically scrape a suitable cover from google images and apply
it as a cover art to the mp3 file.
"""

import argparse
import eyed3
import io
import logging
import os
import re
import tkinter as tk
from PIL import ImageTk, Image
from urllib.error import HTTPError, URLError

from scrape_image_from_google_images import scrape_google_image_on_demand

logging.basicConfig(level=logging.VERBOSE, format='%(message)s')
logging.getLogger().setLevel(logging.VERBOSE)

__all__ = ('add_cover_art', 'add_image')

def wrap(string,length):
    if len(string) > length:
        return string[:length-3]+'...'
    return string 

class tkinter_window:
    is_cancelled = False

    def __init__(self, art_images, song_filename):
        self.song_filename = song_filename
        self.art_images = art_images
        self.current_art_image = next(art_images)

        self.window = tk.Tk()
        self.window.title("Add cover art")
        self.window.geometry("300x210")
        self.window.protocol("WM_DELETE_WINDOW", self.on_cancel)

        filename=os.path.split(self.song_filename)[-1]
        heading = tk.Label(self.window,
                           text='Select cover art for\n' + wrap(filename,15))
        self.image_panel = tk.Label(self.window)
        self.update_image()

        song_query_question = tk.Label(self.window, text='Enter text to search')
        self.song_query = tk.Entry(self.window)

        self.search_button = tk.Button(self.window, text="  Search  ", command=self.on_search)
        apply_button = tk.Button(self.window, text="Apply", command=self.on_apply)
        next_button = tk.Button(self.window, text="Next", command=self.on_next)
        cancel_button = tk.Button(self.window, text="Cancel", command=self.on_cancel)

        heading.grid(column=0, row=0, columnspan=6, rowspan=2)
        self.image_panel.grid(column=0, row=3, columnspan=3, rowspan=3)
        song_query_question.grid(column=3, row=3, columnspan=4, rowspan=1)
        self.song_query.grid(column=3, row=4, columnspan=4, rowspan=1)

        self.search_button.grid(column=4, row=5, columnspan=4, rowspan=1)
        apply_button.grid(column=1, row=6, columnspan=1)
        next_button.grid(column=4, row=6)
        cancel_button.grid(column=5, row=6)

        self.window.mainloop()

    def update_image(self):
        image = ImageTk.PhotoImage(Image.open(io.BytesIO(self.current_art_image)).resize((150, 150), Image.ANTIALIAS))
        self.image_panel.configure(image=image)
        self.image_panel.image = image

    def on_search(self):
        self.search_button.configure(state='disabled', text='Searching..')
        self.window.update()
        song_query = self.song_query.get()
        self.art_images = scrape_google_image_on_demand(song_query + " song cover art", max_num=1)
        self.current_art_image = next(self.art_images)
        self.update_image()
        self.search_button.configure(state='normal', text='Search')

    def on_cancel(self):
        self.is_cancelled = True
        self.window.destroy()

    def on_apply(self):
        add_image(self.current_art_image, self.song_filename)

    def on_next(self):
        self.window.destroy()


def add_image(art_image, song_filename,mime_type='image/jpeg'):
    logging.log(logging.VERBOSE, "Adding cover art: %s", song_filename)
    audiofile = eyed3.load(song_filename)
    if audiofile.tag is None:
        audiofile.initTag()
    elif audiofile.tag.album_artist:
        logging.log(logging.VERBOSE, 'Artist: %s', audiofile.tag.album_artist)
    audiofile.tag.images.set(3, art_image, mime_type)
    audiofile.tag.save()

def get_image(song_filename):
    audiofile = eyed3.load(song_filename)
    try:
        return audiofile.tag.images[0].image_data
    except:
        return None

def extract_query(file_path):
    song_name = os.path.split(file_path)[-1]  # Get songs name from file path
    song_name = song_name.lstrip("0123456789.- ")  # Strip track no and numbers from the song names using lstrip
    song_name = "".join(song_name.split('.')[:-1])  # Remove extension from song names
    song_name = song_name.replace("-", " ").replace("_", " ")
    song_name = re.sub(r"\d\d\d\s*kbps", " ", song_name, flags=re.I)
    song_name = re.sub(r"[\(\[].*?[\)\]]", "", song_name)  # Replace '-','_','320','Kbps','kbps' sign with ' '
    song_name = re.sub(" +", " ", song_name)  # Remove anything in between (),[],{} and replace multiple spaces
    return song_name


def add_cover_art(path='.', no_gui=False, max_num=1,overwrite=False):
    song_filenames = []
    if os.path.isdir(path):
        logging.log(logging.VERBOSE, "Finding all .mp3 files in: %s", path)
        for root, dirs, files in os.walk(path):
            for file in files:
                if file.endswith('.mp3'):
                    song_filenames.append(os.path.join(root, file))
    elif os.path.isfile(path) and args.file.endswith('.mp3'):
        logging.log(logging.VERBOSE, "Finding: %s", path)
        song_filenames.append(os.path.abspath(path))

    for song_filename in song_filenames:
        logging.log(logging.VERBOSE, "Processing file: %s", song_filename)
        song_query = extract_query(song_filename)
        try:
            current_art_image = get_image(song_filename)
            if overwrite or current_art_image is None:
                art_images = scrape_google_image_on_demand(song_query + " song cover art", max_num=max_num)
            else:
                art_images = iter([current_art_image,])
            if not no_gui:
                window = tkinter_window(art_images, song_filename)
                if window.is_cancelled:
                    exit()
            else:
                add_image(next(art_images), song_filename)
        except (HTTPError, URLError, ValueError) as e:
            logging.warning('Unable to download images: %s', e)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('path', nargs='?', default=os.getcwd(),
                        help='file or directory to be processed (default: current directory)')
    parser.add_argument('--max-num', nargs='?', default=1, type=int,
                        help="maximum number of images to be downloaded per query(default: 1)")
    parser.add_argument('--no-gui', action='store_true', help="don't use a gui, automatically add cover art")
    parser.add_argument('--silent', action='store_true', help="don't show console output")
    parser.add_argument('--overwrite', action='store_true', help="overwrite current cover art")

    args = parser.parse_args()

    if args.silent:
        logging.disable()
    add_cover_art(path=args.path, no_gui=args.no_gui, max_num=args.max_num,overwrite=args.overwrite)
