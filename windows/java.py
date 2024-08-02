import os
import subprocess
import sys
import urllib.request
import winreg

def is_java_installed():
    try:
        result = subprocess.run(['java', '-version'], capture_output=True, text=True)
        return 'java version' in result.stderr.lower()
    except FileNotFoundError:
        return False

def download_jdk():
    jdk_url = "https://download.oracle.com/java/21/latest/jdk-21_windows-x64_bin.exe"
    installer_path = os.path.join(os.getcwd(), "jdk_installer.exe")

    print("Downloading JDK 21...")
    urllib.request.urlretrieve(jdk_url, installer_path)
    return installer_path

def install_jdk(installer_path):
    print("Installing JDK 21...")
    subprocess.run([installer_path, "/s"], check=True)

def set_environment_variables():
    print("Setting up environment variables...")

    #Find Java installation directory
    try:
        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\JavaSoft\JDK\21.0.4") as key:
            java_home = winreg.QueryValueEx(key, "JavaHome")[0]
    except WindowsError:
        print("Error: Cannot find Java installation directory")
        return False

    #Set JAVA_HOME
    os.environ['JAVA_HOME'] = java_home
    subprocess.run(f'setx JAVA_HOME "{java_home}"', shell=True, check=True)

    #Update PATH
    path = os.environ['PATH']
    java_bin = os.path.join(java_home, 'bin')
    if java_bin not in path:
        new_path = f"{java_bin};{path}"
        os.environ['PATH'] = new_path
        subprocess.run(f'setx PATH "{new_path}"', shell=True, check=True)

    return True


def main():
    if is_java_installed():
        print("Java is already installed.")
        return
    else:
        print("Java is not installed.")
    
    if os.name != "nt" or sys.platform != "win32":
        print("This script is designed for Windows only")
        print(f"{os.name} {sys.platform}")
        return

    if os.name == "nt" and sys.getwindowsversion().build < 22000:
        print("This script is designed for Windows 11. Your version might not be compatible.")
        return

    try:
        installer_path = download_jdk()
        install_jdk(installer_path)
        if set_environment_variables():
            print("Java 21 has been successfully installed and configured.")
            return
        else:
            print("Java 21 installation completed, but environment variables setup failed.")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        if os.path.exists(installer_path):
            os.remove(installer_path)

if __name__ == "__main__":
    main()
