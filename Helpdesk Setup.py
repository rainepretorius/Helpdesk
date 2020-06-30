import os

os.system("if not exist C:\ProgramData\Helpdesk mkdir C:\ProgramData\Helpdesk")
cwd = os.getcwd()
h= "Helpdesk"
shortcut = "Start_Helpdesk.lnk"
copydir = f"{cwd}\{h}"
os.system(f'xcopy "{copydir}" "C:\ProgramData\Helpdesk"')
os.system(f'xcopy "{copydir}\{shortcut}" "%userprofile%\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup"')
os.system(f'xcopy "{copydir}\{shortcut}" "C:\ProgramData\Microsoft\Windows\Start Menu\Programs"')
