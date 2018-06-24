from PIL import ImageTk, Image
import tkinter as tk
window = tk.Tk()
window.title("Add cover art")
#window.geometry("600x500")
name = tk.Label(window,text='Do u want this images as cover art' )
path = "./images/Capital+Cities+Safe+and+Sound+song+cover+art_0.jpg"
img = ImageTk.PhotoImage(Image.open(path))
panel = tk.Label(window, image = img)
song_query_question = tk.Label(window,text='Enter text to search' )
song_query = tk.Entry(window)
OK= tk.Button(window, text="Okay")
Cancel = tk.Button(window, text="Cancel")
Next= tk.Button(window, text="Next")

name.grid(column=0,row=0,columnspan=6)
panel.grid(column=0,row=1,columnspan=3,rowspan =3)
OK.grid(column=0,row=4,columnspan=2)
Next.grid(column=2,row=4)
song_query_question.grid(column=3,row=1,columnspan=3)
song_query.grid(column=3,row=2,columnspan=3)
Cancel.grid(column=4,row=4,columnspan=2)

window.mainloop()





    