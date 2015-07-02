import os

f = []
for (dirpath, dirnames, filenames) in os.walk('weibo'):
    f.extend(filenames)
    break

counter = 802
for img in f:
    if img == '.DS_Store':
        continue
    counter += 1
    os.rename('weibo/%s' % img, 'weibo/p%d.jpg' % counter)


