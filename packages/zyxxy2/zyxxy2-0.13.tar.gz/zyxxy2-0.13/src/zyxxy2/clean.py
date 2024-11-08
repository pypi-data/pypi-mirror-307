import os

for dir_ in ['__pycache__', ] + [os.path.join('test_files', 'test_'+d) for d in ["drawings", "images", "videos"]]: # 'images_videos'
  if not os.path.isdir(dir_):
    continue
  for file_ in os.listdir(dir_):
    os.remove(os.path.join(dir_, file_))
if os.path.isfile('MY_demo_DUMP.py'):
  os.remove('MY_demo_DUMP.py') 

from matplotlib import get_cachedir
cache_dir = get_cachedir()
print(cache_dir)