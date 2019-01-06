#!/usr/bin/python3
# -*- coding: utf-8 -*-
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
import itertools
import tkinter as tk
from tkinter import ttk
from PIL import ImageTk, Image

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
        self.cached_images=[next(art_images)]
        self.current_art_index = 0

        self.window = tk.Tk()
        self.window.title("Add Cover Art")
        self.window.geometry("450x250")
        self.window.protocol("WM_DELETE_WINDOW", self.on_cancel)
        self.window.resizable(width=False, height=False)

        filename=os.path.split(self.song_filename)[-1]
        heading = tk.Label(self.window,
                           text='Select cover art for\n' + wrap(filename,40))
        self.image_panel = ttk.Label(self.window)
        self.update_image()

        song_query_question = ttk.Label(self.window, text='Enter Search Text')
        self.song_query = ttk.Entry(self.window)
        self.song_query.bind('<Return>', self.on_search)

        self.search_button = ttk.Button(self.window, text="Search", command=self.on_search)
        apply_button = ttk.Button(self.window, text="Apply", command=self.on_apply)
        front_button = ttk.Button(self.window, text="⇨", command=self.on_front)
        back_button = ttk.Button(self.window, text="⇦", command=self.on_back)
		
        next_button = ttk.Button(self.window, text="Next", command=self.on_next)
        cancel_button = ttk.Button(self.window, text="Cancel", command=self.on_cancel)

        heading.grid(column=0, row=0, columnspan=6, rowspan=2, pady=(10,10))
        self.image_panel.grid(column=0, row=3, columnspan=3, rowspan=3, pady=(0,10))
        song_query_question.grid(column=3, row=3, columnspan=4, rowspan=1)
        self.song_query.grid(column=3, row=4, columnspan=4, rowspan=1)

        self.search_button.grid(column=4, row=5, columnspan=4, rowspan=1)
        apply_button.grid(column=1, row=6, columnspan=1)
        front_button.grid(column=2, row=6, columnspan=1, padx=(0,10))
        back_button.grid(column=0, row=6, columnspan=1, padx=(10,0))
        next_button.grid(column=4, row=6)
        cancel_button.grid(column=5, row=6)

        self.window.mainloop()

    def on_back(self):
        self.current_art_index -= 1
        if self.current_art_index<0:
            self.current_art_index = len(self.cached_images)-1
        self.update_image()


    def on_front(self):
        try:
            self.cached_images.append(next(self.art_images))
        except StopIteration:
            pass
        self.current_art_index += 1
        if self.current_art_index >= len(self.cached_images):
            self.current_art_index=0
        self.update_image()


    def update_image(self):
        current_art_image = self.cached_images[self.current_art_index]
        image = ImageTk.PhotoImage(Image.open(io.BytesIO(current_art_image)).resize((150, 150), Image.ANTIALIAS))
        self.image_panel.configure(image=image)
        self.image_panel.image = image

    def on_search(self,*args):
        self.search_button.configure(state='disabled', text='Searching..')
        self.window.update()
        song_query = self.song_query.get()
        try:
            self.art_images = scrape_google_image_on_demand(song_query + " song cover art")
            self.cached_images = [next(self.art_images)]
            self.current_art_index = 0
        except StopIteration:
            pass
        self.update_image()
        self.search_button.configure(state='normal', text='Search')

    def on_cancel(self):
        self.is_cancelled = True
        self.window.destroy()

    def on_apply(self):
        add_image(self.cached_images[self.current_art_index], self.song_filename)

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


def add_cover_art(path='.', no_gui=False, overwrite=False):
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
            art_images = scrape_google_image_on_demand(song_query + " song cover art")
            if not overwrite and current_art_image is not None:
                art_images = itertools.chain([current_art_image],art_images)
            if not no_gui:
                window = tkinter_window(art_images, song_filename)
                if window.is_cancelled:
                    exit()
            else:
                next(art_images)
                add_image(next(art_images), song_filename)
        except StopIteration as e:
            logging.warning('Unable to download images: %s', e)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__, epilog="if no optional argument is specified, the gui is enabled and overwrite is disabled")
    parser.add_argument('path', nargs='?', default=os.getcwd(),
                        help='file or directory to be processed (default: current directory)')
    parser.add_argument('--silent', action='store_true', help="don't show console output")
    
    group = parser.add_mutually_exclusive_group()
    group.add_argument('--no-gui', action='store_true', help="don't use a gui and overwrite current cover art from a list of choices")
    group.add_argument('--overwrite', action='store_true', help="use gui and overwrite current cover art from a list of choices")

    args = parser.parse_args()

    if args.silent:
        logging.disable()
    add_cover_art(path=args.path, no_gui=args.no_gui, overwrite=args.overwrite)
