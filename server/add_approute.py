import time
import os

time.sleep(15)
cwd = os.getcwd()
uiloc = "uiserver1.py"
location = f'{cwd}\{uiloc}'
py = open(location, "r")
ui = py.readlines()
py.close()
lnk = open("../approute.config")
resetlink = lnk.readline()
lnk.close()
final = []
for i in ui:
    final.append(i)
time.sleep(2)
final[569] = f'@app.route("/{resetlink}")\n'
if os.path.isfile(location):
    os.remove(location)
uiwrite = open(location, "w+")
uiwrite.seek(0)
for j in final:
    uiwrite.writelines(j)
uiwrite.close()
pythonpath = f'python "{location}"'
os.system(pythonpath)
print("Done")
