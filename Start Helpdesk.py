import os
import time

cwd = os.getcwd()
u = "UI-Server.exe"
n = "Notify.exe"
ui = f"{cwd}\{u}"
notify = f"{cwd}\{n}"

os.system(notify)
time.sleep(5)
os.system(ui)
