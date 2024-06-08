import json
import os
import datetime
import tarfile
from termcolor import colored
from standard import wait_clear, exit_menu, Invalid

with open("../xsf-config.json") as f:
    config = json.load(f)

current_datetime = datetime.datetime.now()
date_format = "%Y-%m-%d_%H-%M-%S"


class BackupFunction:
    def pack(self, archive_name, files):
        directory_name = current_datetime.strftime(date_format)
        os.makedirs(config["backup"][0]["backup_path"] + directory_name)

        with tarfile.open(archive_name, 'w:gz') as tar:
            for file in files:
                tar.add(file)

        self.pack(directory_name, config["backup"][0]["files"])

    def unpack(self, archive_name, destination_path="/"):
        with tarfile.open(archive_name, "r:gz") as tar:
            tar.extractall(path=destination_path)

        self.unpack(archive_name, destination_path)

    def display_files(self, location=config["backup"][0]["backup_path"]):
        print(colored("Backup: ", "green"), location)
        for item in os.listdir(location):
            print(item)

        self.display_files(location)


def backupMenu():
    wait_clear()
    print(colored('Backup Menu', 'green'))
    backupMenu = {
        "1": ("Packing", BackupFunction.pack),
        "2": ("Unpacking", BackupFunction.unpack),
        "3": ("Show backup list", BackupFunction.display_files),
        "q": ("Exit", exit_menu)
    }

    for backupKey in sorted(backupMenu.keys()):
        print(backupKey + colored(" -> ", "green") + backupMenu[backupKey][0])

    selectBackup = input(colored(">> ", "green"))
    backupMenu.get(selectBackup, [None, Invalid])[1]()
