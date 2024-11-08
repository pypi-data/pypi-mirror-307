import os
import sys
import subprocess
import time
from rich import print


version_list = ['3.9', '3.10', '3.11', '3.12', '3.13', '3.13t']
script_path = os.path.abspath(__file__)
filedir = os.path.dirname(script_path)
if os.name == 'nt':
    temp_dir = os.path.expanduser("~/AppData/Local/Temp")
else:
    temp_dir = "/tmp"

help_str = """
[red]欢迎来到 Python Version[/]

命令列表:

  [green]【pyvv help】[/]           查看帮助
  [green]【pyvv list】[/]           查看已安装/可安装
  [green]【pyvv 3.13】[/]           安装/进入 Python3.13, 其他版本以此类推
  [green]【pyvv 3.13 pip】[/]       运行 Python3.13 的 pip 命令
  [green]【pyvv 3.13 -m pip】[/]    运行 Python3.13 的 pip 命令
  [green]【pyvv 3.13 run pip】[/]   运行 Python3.13 的 pip 命令
  [green]【pyvv 3.13 run uv】[/]    运行 Python3.13 的 uv 命令（如果已安装）
  [green]【pyvv 3.13 hello.py】[/]  通过 Python3.13 运行脚本 hello.py
  [green]【pyvv remove 3.13】[/]    删除 Python3.13
"""

def main():
    args = sys.argv
    
    if len(args) > 1:
        if args[1] in version_list:
            version = args[1]
            if os.name == 'nt':
                script_path = os.path.join(filedir, version, 'Scripts')
                python_path = os.path.join(script_path, 'python.exe')
                pip_path = os.path.join(script_path, 'pip3.exe')
            else:
                script_path = os.path.join(filedir, version, 'bin')
                python_path = os.path.join(script_path, 'python')
                pip_path = os.path.join(script_path, 'pip3')
            
            if not os.path.exists(python_path):
                print(f'python{version} installing...')
                z = os.system(f'uv venv {filedir}/{version} -p {version}')
                if z == 0:
                    print(f'python{version} installed')
                else:
                    print(f'python{version} installing failed.')
                    return
            if not os.path.exists(pip_path):
                print(f'pip installing...')
                subprocess.getoutput(f'{python_path} -m ensurepip')
                print('pip installed')
            if len(args) > 2:
                if args[2] == 'run':
                    if len(args) > 3:
                        if args[3] == 'pip' or args[3] == 'pip.exe':
                            args[3] = 'pip3'
                        cmd = os.path.join(script_path, args[3])
                        if len(args) > 4:
                            cmd = ' '.join([cmd, *args[4:]])
                        return os.system(cmd)
                    print(help_str)
                    return
                elif args[2] == 'pip' or args[2] == 'pip.exe':
                    args[2] = 'pip3'
                    cmd = os.path.join(script_path, args[2])
                    if len(args) > 3:
                        cmd = ' '.join([cmd, *args[3:]])
                    return os.system(cmd)
                cmd = ' '.join([python_path, *args[2:]])
                return os.system(cmd)
            try:
                return os.system(python_path)
            except KeyboardInterrupt:
                pass
        elif args[1] == 'list':
            z = os.listdir(filedir)
            installed = [i for i in version_list if i in z]
            noinstalled = [i for i in version_list if i not in z]
            print(f"已安装的Python版本有: [green]{installed}[/]")
            print(f"未安装的Python版本有: [red]{noinstalled}[/]")
            return
        elif args[1] in ['help', '--help', '-h']:
            print(help_str)
            return
        elif args[1] in ['remove']:
            if len(args) > 2:
                if args[2] not in version_list:
                    print(f'[red]只能删除支持的版本号 {version_list}[/]')
                    return
                if args[2] not in os.listdir(filedir):
                    return f"Python{args[2]} 不存在"
                os.renames(os.path.join(filedir, args[2]), os.path.join(temp_dir, f"{args[2]}-{time.time():.0f}"))
                print(f'[green]{args[2]} 已删除[/]')
                return
            print(help_str)
            return
        else:
            print(f"支持的Python版本有 {version_list}")
            return
    else:
        print(help_str)