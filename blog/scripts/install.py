import os
import sys

PYH_FILE = 'geek-blog.pth'

if __name__ == '__main__':
    paths = filter(lambda p: p.endswith('dist-packages'), sys.path)
    if len(paths) > 0:
        dist_path = paths[0]
        pth_path = os.path.join(dist_path, PYH_FILE)
        if os.path.exists(pth_path):
            os.remove(pth_path)
        with open(PYH_FILE, "w+") as fp:
            fp.write(os.getcwd())
            fp.write('\n')
            fp.write(os.path.join(os.getcwd(), 'geekblog'))
        print 'Modifying python path...'
        os.link(PYH_FILE, pth_path)
