import os
import subprocess
import sys

def main():
    # 创建虚拟环境
    venv_name = "venv"
    subprocess.run([sys.executable, "-m", "venv", venv_name])

    # 安装requirements.txt中的包
    requirements_file = "requirements.txt"
    venv_python = os.path.join(venv_name, "Scripts", "python.exe" if os.name == 'nt' else "bin/python3")

    if os.path.exists(requirements_file):
        subprocess.run([venv_python, "-m", "pip", "install", "-r", requirements_file])
    else:
        print(f"{requirements_file} not found in the current directory.")

if __name__ == "__main__":
    main()