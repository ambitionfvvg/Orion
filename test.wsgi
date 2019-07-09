import sys

#app's path
sys.path.insert(0,r"C:\Users\zhaohui.li\Desktop\zpl\print_label")

from label1 import app

#Initialize WSGI app object
application = app