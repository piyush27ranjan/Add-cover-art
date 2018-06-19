import os
import eyed3

asps = []
for root, dirs, files in os.walk(r'D:\\'):
    for file in files:
        if file.endswith('.mp3'):
            asps.append(os.path.join(root, file))