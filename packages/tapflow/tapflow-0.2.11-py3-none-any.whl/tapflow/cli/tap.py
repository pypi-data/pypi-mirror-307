import os
import sys
import subprocess
from IPython import start_ipython

def activate_virtualenv():
    """激活虚拟环境"""
    if os.name == 'nt':  # Windows
        activate_script = '.venv\\Scripts\\activate'
    else:  # macOS/Linux
        activate_script = 'source .venv/bin/activate'
    
    # 激活虚拟环境
    os.system(activate_script)

def main():
    # 获取当前脚本所在的目录
    basepath = os.path.dirname(os.path.abspath(__file__))

    # 检查是否在源代码环境中
    if os.path.isdir(os.path.join(basepath, "tapflow")):
        # 源代码环境
        source_path = os.path.join(basepath, "tapflow")
        # 检查并创建虚拟环境
        if not os.path.isdir(".venv"):
            os.system("python -m venv .venv")
            activate_virtualenv()
            os.system("pip install -r requirements.txt")
        activate_virtualenv()
    else:
        # 安装后的环境，动态获取安装路径
        source_path = subprocess.check_output(
            "python -c \"import os, tapflow; print(os.path.dirname(tapflow.__file__))\"",
            shell=True
        ).decode().strip()

    # 设置环境变量, 兼容 Windows
    os.environ["LC_ALL"] = "en_US.utf8"

    # 检查 ipython3 是否安装
    try:
        subprocess.check_output("which ipython3", shell=True, stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError:
        print("NO ipython3 found, please run pip3 install -r requirements.txt before use tapcli")
        sys.exit(1)

    # 启动 IPython 交互式 shell，加载配置
    ipython_config_path = os.path.join(basepath, '.cli', 'ipython_config.py')
    if not os.path.exists(ipython_config_path):
        os.makedirs(os.path.dirname(ipython_config_path), exist_ok=True)
        with open(ipython_config_path, 'w') as f:
            f.write('''c = get_config()  #noqa
from IPython.terminal.prompts import Prompts, Token

class NoPrompt(Prompts):
    def in_prompt_tokens(self, cli=None):
        return [(Token.Prompt, 'tap > ')]

    def out_prompt_tokens(self):
        return [(Token.OutPrompt, 'tap > ')]

c.TerminalInteractiveShell.prompts_class = NoPrompt
''')

    start_ipython(argv=['--no-banner', '--profile-dir=.cli', '--profile=ipython_config', '-i', os.path.join(source_path, 'cli', 'cli.py')])

if __name__ == "__main__":
    main() 