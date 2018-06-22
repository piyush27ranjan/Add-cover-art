from PIL import ImageTk, Image
import tkinter as tk
window = tk.Tk()
window.title("Add cover art")
window.geometry("800x500")
window.configure(background='grey')

path = "./images/Capital+Cities+Safe+and+Sound+song+cover+art_0.jpg"
img = ImageTk.PhotoImage(Image.open(path))
panel = tk.Label(window, image = img)
panel.pack(side = "bottom", fill = "both", expand = "yes")
window.mainloop()





    