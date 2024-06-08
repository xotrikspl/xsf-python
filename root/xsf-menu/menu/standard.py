import json
import subprocess
import time
from pathlib import Path

with open('../xsf-config.json') as f:
    config = json.load(f)


def Invalid():
    print("Invalid!")
    raise SystemExit


def wait_clear():
    time.sleep(0.25)
    subprocess.run("clear", check=True)


def exit_menu():
    raise SystemExit


class ServerFunction:
    def clear_logs(self):
        def should_ignore(file_path):
            for ignore_path in config["server"][0]["ignore_paths"]:
                if file_path.is_relative_to(ignore_path):
                    return True
            return False

        for pattern in config["server"][0]["files_to_delete"]:
            for file_path in Path(config["server"][0]["xsf"]).rglob(pattern):
                if pattern == "*.txt" and should_ignore(file_path):
                    print(f"I ignore the file: {file_path}")
                    continue

                result = subprocess.run(["rm", "-f", str(file_path)], capture_output=True, text=True)
                if result.returncode == 0:
                    print(f"File deleted: {file_path}")
                else:
                    print(f"Error deleting file {file_path}: {result.stderr}")
