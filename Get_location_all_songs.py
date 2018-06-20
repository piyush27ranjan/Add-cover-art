import os
import eyed3
import scrape_image_from_google_images

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
    scrape_image_from_google_images.scrape_google_image(music_names[i][0]+" song cover art")