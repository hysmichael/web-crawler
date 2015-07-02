
import urllib

size = 180
while True:
    url = 'http://tp2.sinaimg.cn/3669120105/%d/5722790741/0' % size
    filename, headers = urllib.urlretrieve(url)
    if headers['Content-Type'] == 'text/html':
        print '   %d' % size
    else:
        print ' + %d' % size
    size += 1