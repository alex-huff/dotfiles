import os, time
date = time.time_ns()
imageName = f'screenshot-{date}.png'
os.system(f'grimshot save area {imageName}')
os.system(f'imgur-uploader {imageName}')

