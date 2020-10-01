import os
import time
from server import ui-server1.py
from notification import notify1.py


notify1.run()
time.sleep(5)
ui-server1.run()
