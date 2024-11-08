import os
import subprocess

def run_init_script():
    script_path = os.path.join(os.path.dirname(__file__), '../scripts/init_env.sh')
    if os.path.isfile(script_path):
        try:
            # 使用 sudo 运行 init_env.sh
            subprocess.run(['sudo', 'bash', script_path], check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error occurred while executing init_env.sh: {e}")
    else:
        print("Script init_env.sh does not exist.")

def main():
    print("Starting the LinkLinux Init tool...")
    run_init_script()

if __name__ == "__main__":
    main()

