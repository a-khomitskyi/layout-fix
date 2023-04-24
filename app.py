import platform
import subprocess

os_name = platform.system()

if __name__ == '__main__':
    if os_name == 'Windows':
        subprocess.run(['python', 'for-windows-fix.py'])
    elif os_name == 'Linux':
        subprocess.run(['python', 'for-linux-fix.py'])
    else:
        print("Sorry, your OS isn't supported =(")
