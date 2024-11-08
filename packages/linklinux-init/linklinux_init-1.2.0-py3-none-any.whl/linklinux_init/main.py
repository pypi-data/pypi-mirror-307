import os
import subprocess

SCRIPTS_BASE_URL = "http://linuxconfig.suyelu.com/data/linux"  # 替换为你自己的服务器地址
SCRIPTS = ["init_env.sh", "linklinux_env.sh", "install_vim.sh", "install_zsh.sh"]

def download_script(script_name):
    script_url = f"{SCRIPTS_BASE_URL}/{script_name}"
    script_path = os.path.join(os.getcwd(), script_name)  # 下载到当前工作目录

    try:
        # 使用 wget 下载脚本
        subprocess.run(['wget', '-q', '-O', script_path, script_url], check=True)
        # 设置脚本为可执行
        os.chmod(script_path, 0o755)
        print(f"{script_name} 下载成功并设置为可执行。")
    except subprocess.CalledProcessError as e:
        print(f"下载 {script_name} 时出错: {e}")
        exit(1)

def run_script(script_name):
    script_path = os.path.join(os.getcwd(), script_name)  # 从当前工作目录运行
    if os.path.isfile(script_path):
        try:
            # 使用 sudo 运行脚本
            subprocess.run(['sudo', 'bash', script_path], check=True)
        except subprocess.CalledProcessError as e:
            print(f"执行 {script_name} 时出错: {e}")
    else:
        print(f"Script {script_name} does not exist.")

def main():
    print("Starting the LinkLinux Init tool...")

    # 下载所有需要的脚本
    for script in SCRIPTS:
        download_script(script)

    # 执行 init_env.sh 脚本
    run_script('init_env.sh')

if __name__ == "__main__":
    main()
