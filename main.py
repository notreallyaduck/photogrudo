import sys
import time

from cefpython3 import cefpython as cef
import os
import shutil


def main():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(current_dir)
    code_dir = current_dir + "/src"

    if not os.path.exists("%AppData%/Photogrudo"):
        shutil.copytree(code_dir, "%AppData%/Photogrudo")

    os.chdir("%AppData%/Photogrudo")

    os.system('START /B start_server.vbs')

    time.sleep(2)

    sys.excepthook = cef.ExceptHook  # To shutdown all CEF processes on error
    cef.Initialize()
    cef.CreateBrowserSync(url="http://localhost:8501", window_title="Photogrudo")
    cef.MessageLoop()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()
