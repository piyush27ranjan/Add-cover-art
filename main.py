"""
Add Cover Art:
This application will find the .mp3 files in your computer.
Then it will automatically scrape a suitable cover from google images and apply
it as a cover art to the mp3 file.
"""

import re
import os
import argparse
from urllib.error import HTTPError,URLError
import tkinter as tk

from scrape_image_from_google_images import scrape_google_image
from PIL import ImageTk, Image
import eyed3

    

def tkinter_window(location, audiofile):
    inputs={}
    def get_entry():
        inputs['song_query']=song_query.get()
        window.destroy()
    window = tk.Tk()
    window.title("Add cover art")
    window.geometry("300x250")
    name = tk.Label(window, text='Do you want this images as cover art')
    path = location
    img = ImageTk.PhotoImage(Image.open(path).resize((150, 150), Image.ANTIALIAS))
    panel = tk.Label(window, image=img)
    song_query_question = tk.Label(window, text='Enter text to search')
    song_query = tk.Entry(window)
    OK = tk.Button(window, text="Okay", command=add_image(location, audiofile))

    Cancel = tk.Button(window, text="Cancel", command=window.destroy)
    Search = tk.Button(window, text="Search", command=get_entry)

    name.grid(column=0, row=0, columnspan=6)
    panel.grid(column=0, row=1, columnspan=3, rowspan=3)
    OK.grid(column=0, row=4, columnspan=2)
    Search.grid(column=2, row=4)
    song_query_question.grid(column=3, row=1, columnspan=3)
    song_query.grid(column=3, row=2, columnspan=3)
    Cancel.grid(column=4, row=4, columnspan=2)

    window.mainloop()


    return inputs


def add_image(location, audiofile):
    if (audiofile.tag is None):
        audiofile.initTag()
    print(audiofile.tag.album_artist)
    audiofile.tag.images.set(3, open(location, 'rb').read(), 'image/jpeg')
    audiofile.tag.save()


if __name__ == '__main__':


    parser = argparse.ArgumentParser()
    parser.add_argument('file', nargs='?', default=os.getcwd())
    parser.add_argument('--no-gui', action='store_true',help='dont use a gui, automatically add cover art')
    args=parser.parse_args()

    song_paths = []
    if os.path.isdir(args.file):
        print("Finding all .mp3 files in:", args.file)
        for root, dirs, files in os.walk(args.file):
            for file in files:
                if file.endswith('.mp3'):
                    song_paths.append(os.path.join(root, args.file))
    elif os.path.isfile(args.file) and args.file.endswith('.mp3'):
        print("Finding:", args.file)
        song_paths.append(os.path.abspath(args.file))

    # Get songs name with location
    music_names = []
    for i in range(len(song_paths)):
        music_names.append([])
        music_names[i].append(os.path.split(song_paths[i])[-1])
        music_names[i].append(song_paths[i])

    # Strip track no and numbers from the song names using lstrip
    for i in range(len(music_names)):
        music_names[i][0]=music_names[i][0].lstrip("0123456789.- ")

        # Remove extension from song names
    for i in range(len(music_names)):
        music_names[i][0] = "".join(music_names[i][0].split('.')[:-1])

        # replace '-','_','320','Kbps','kbps' sign with ' '
    for i in range(len(music_names)):
        music_names[i][0] = music_names[i][0].replace("-", " ")
        music_names[i][0] = music_names[i][0].replace("_", " ")
        music_names[i][0] = re.sub("\d\d\d\s*kbps"," ", music_names[i][0], flags=re.I)

        # remove anything in between (),[],{} and replace multiple spaces
    for i in range(len(music_names)):
        music_names[i][0] = re.sub(r"[\(\[].*?[\)\]]", "", music_names[i][0])
        music_names[i][0] = re.sub(" +"," ", music_names[i][0])


    for i in range(len(music_names)):
        audiofile = eyed3.load(music_names[i][1])
        try:
            song_directory = scrape_google_image(music_names[i][0] + " song cover art", name=music_names[i][0],
                                             max_num=1)
        except (HTTPError,URLError):
            print ('Unable to Download the images')
            continue
        song_filename = os.path.join(song_directory, os.listdir(song_directory)[0])
        Image.open(song_filename)
        if args.no_gui:
            add_image(song_filename,audiofile)
        else:
            while True:
                inputs=tkinter_window(song_filename, audiofile)
                if inputs:
                    try:
                        song_directory = scrape_google_image(inputs['song_query'] + " song cover art", name=inputs['song_query'] ,
                                                        max_num=1)
                    except (HTTPError,URLError):
                        print ('Unable to Download the images')
                        continue
                    song_filename = os.path.join(song_directory, os.listdir(song_directory)[0])
                else:
                    break
                    
