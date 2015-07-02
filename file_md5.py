import os
import hashlib

f = []
for (dirpath, dirnames, filenames) in os.walk('weibo'):
    f.extend(filenames)
    break

d = {}
for img in f:
    md5 = hashlib.md5(open('weibo/%s' % img, 'rb').read()).hexdigest()
    if md5 in d:
        d[md5] += 1
    else:
        d[md5] = 1

import operator
sorted_d = sorted(d.items(), key=operator.itemgetter(1))

black_list = []

for key, value in sorted_d:
    if value > 1:
        black_list.append(key)

for img in f:
    md5 = hashlib.md5(open('weibo/%s' % img, 'rb').read()).hexdigest()
    if md5 in black_list:
        os.remove('weibo/%s' % img)

print "'" + "', '".join(black_list) + "'"
