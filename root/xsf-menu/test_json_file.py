import json
import subprocess
import time

with open("xsf-config.json") as f:
    config = json.load(f)


def run_command(command, log_file):
    with open(log_file, "a") as f:
        subprocess.Popen(command, stdout=f, stderr=subprocess.STDOUT, shell=True)
    time.sleep(0.5)


def twoTestFile():
    start_channel = int(input("> "))

    for ch in range(1, start_channel + 1):
        channel_path = config["server"][0]["xsf_channel"] + f"/ch{ch}"
        pchannel_path = config["server"][0]["xsf_channel"] + f"/ch{ch}/pch{ch}"

        print(f"Starting on CH/pCH{ch}")
        print(channel_path)
        print(pchannel_path)


twoTestFile()
