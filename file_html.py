import os

print '''<html><head><script>
function print(image) {
    console.log('rm -f weibo/i' + image.getAttribute('title') + '.jpg');
    image.setAttribute('style', 'display:none');
}
</script></head><body>'''

f = []
for (dirpath, dirnames, filenames) in os.walk('weibo'):
    f.extend(filenames)
    break

counter = 0
for img in f:
    if img == '.DS_Store':
        continue
    img_id = int(img[1:-4])
    if img_id in range(1001, 2000):
        print '<img src="weibo/i%d.jpg" alt="" width=100px title="%d" onClick="print(this)">' % (img_id, img_id)

print "</body></html>"
