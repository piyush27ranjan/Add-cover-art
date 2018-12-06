import re
import os
import eyed3
import scrape_image_from_google_images
from PIL import ImageTk, Image
import tkinter as tk
import argparse



def tkinter_window(location, audiofile):
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
    Next = tk.Button(window, text="Next", command=window.destroy)

    name.grid(column=0, row=0, columnspan=6)
    panel.grid(column=0, row=1, columnspan=3, rowspan=3)
    OK.grid(column=0, row=4, columnspan=2)
    Next.grid(column=2, row=4)
    song_query_question.grid(column=3, row=1, columnspan=3)
    song_query.grid(column=3, row=2, columnspan=3)
    Cancel.grid(column=4, row=4, columnspan=2)

    window.mainloop()


def add_image(location, audiofile):
    if (audiofile.tag is None):
        audiofile.initTag()
    print(audiofile.tag.album_artist)
    audiofile.tag.images.set(3, open(location, 'rb').read(), 'image/jpeg')
    audiofile.tag.save()


if __name__ == '__main__':
    
    parser = argparse.ArgumentParser()
    parser.add_argument('directory', nargs='?', default=os.getcwd())
    args=parser.parse_args()
    
    print("Finding all .mp3 files in ",args.directory)
    asps = []        
    for root, dirs, files in os.walk(args.directory):
        for file in files:
            if file.endswith('.mp3'):
                asps.append(os.path.join(root, file))
    print(len(asps),' Files Found, Processing...')
    
    # Get songs name with location
    music_names = []
    for i in range(len(asps)):
        music_names.append([])
        music_names[i].append(os.path.split(asps[i])[-1])
        music_names[i].append(asps[i])

    # Strip track no and numbers from the song names
    # Get list of numbers
    num = []
    for i in range(10):
        num.append(str(i))
    num.append("-")
    for i in range(len(music_names)):
        for a in music_names[i][0]:
            if a in num:
                music_names[i][0] = music_names[i][0][1:]
            else:
                break

        # Remove extension from song names
    for i in range(len(music_names)):
        music_names[i][0] = "".join(music_names[i][0].split('.')[:-1])

        # replace '-','_','320','Kbps','kbps' sign with ' '
    for i in range(len(music_names)):
        music_names[i][0] = music_names[i][0].replace("-", " ")
        music_names[i][0] = music_names[i][0].replace("_", " ")
        music_names[i][0] = music_names[i][0].replace("320", " ")
        music_names[i][0] = music_names[i][0].replace("Kbps", " ")
        music_names[i][0] = music_names[i][0].replace("kbps", " ")

        # remove anything in between (),[],{}
    for i in range(len(music_names)):
        music_names[i][0] = re.sub(r"[\(\[].*?[\)\]]", "", music_names[i][0])

    for i in range(len(music_names)):
        audiofile = eyed3.load(music_names[i][1])
        song_file_name = scrape_image_from_google_images.scrape_google_image(music_names[i][0] +
                                                                             " song cover art", name=music_names[i][0])
        Image.open(song_file_name)
        tkinter_window(song_file_name, audiofile)
