import os
import eyed3
import scrape_image_from_google_images
from PIL import ImageTk, Image
import tkinter as tk

def tkinter_window(location):
    window = tk.Tk()
    window.title("Add cover art")
    #window.geometry("600x500")
    name = tk.Label(window,text='Do u want this images as cover art' )
    path = location
    img = ImageTk.PhotoImage(Image.open(path))
    panel = tk.Label(window, image = img)
    song_query_question = tk.Label(window,text='Enter text to search' )
    song_query = tk.Entry(window)
    OK= tk.Button(window, text="Okay",command = add_image(location))
    Cancel = tk.Button(window, text="Cancel")
    Next= tk.Button(window, text="Next",command = window.destroy)
    
    name.grid(column=0,row=0,columnspan=6)
    panel.grid(column=0,row=1,columnspan=3,rowspan =3)
    OK.grid(column=0,row=4,columnspan=2)
    Next.grid(column=2,row=4)
    song_query_question.grid(column=3,row=1,columnspan=3)
    song_query.grid(column=3,row=2,columnspan=3)
    Cancel.grid(column=4,row=4,columnspan=2)
    
    window.mainloop()

def add_image(location):
    print('hello')

asps = []
for root, dirs, files in os.walk(r'D:\\'):
    for file in files:
        if file.endswith('.mp3'):
            asps.append(os.path.join(root, file))

     
       #Get songs name with location 
music_names = []
for i in range(len(asps)):
    music_names.append([])
    music_names[i].append(asps[i].split("\\")[-1])
    music_names[i].append(asps[i])
    

      #Strip track no and numbers from the song names
#Get list of numbers
num = []
for i in range(10):
    num.append(str(i))
num.append("-")
for i in range(len(music_names)):
    for a in music_names[i][0]:
        if a in num :
            music_names[i][0] = music_names[i][0][1:]
        else:
            break
        
    #Remove extension from song names
for i in range(len(music_names)):
    music_names[i][0] = "".join(music_names[i][0].split('.')[:-1])     

    #replace '-','_','320','Kbps','kbps' sign with ' '
for i in range(len(music_names)):
    music_names[i][0] = music_names[i][0].replace("-"," ")
    music_names[i][0] = music_names[i][0].replace("_"," ")
    music_names[i][0] = music_names[i][0].replace("320"," ")
    music_names[i][0] = music_names[i][0].replace("Kbps"," ")
    music_names[i][0] = music_names[i][0].replace("kbps"," ")
        
    #remove anything in between (),[],{}
import re 
for i in range(len(music_names)):
    music_names[i][0] = re.sub("[\(\[].*?[\)\]]", "", music_names[i][0])

for i in range(len(music_names)):
    audiofile = eyed3.load(music_names[i][1])
    song_file_name=scrape_image_from_google_images.scrape_google_image(music_names[i][0]+    \
                                                        " song cover art",name=music_names[i][0])
    tkinter_window(song_file_name)
    
    