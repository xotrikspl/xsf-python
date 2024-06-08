import json
import subprocess
import time
from termcolor import colored
from pathlib import Path
import standard as std
from standard import ServerFunction

serverfnc = ServerFunction()

with open("../xsf-config.json") as f:
    config = json.load(f)


def serverMenu():
    std.wait_clear()
    print(colored('Server Menu', 'green'))
    server = {
        "1": ("Start server", ServerFunctions.startServer),
        "2": ("Stop server", ServerFunctions.stopServer),
        "q": ("Exit", std.exit_menu)
    }

    for serverKey in sorted(server.keys()):
        print(serverKey + colored(" -> ", "green") + server[serverKey][0])

    selectServer = input(colored(">> ", "green"))
    server.get(selectServer, [None, std.Invalid])[1]()


class ServerFunctions:

    def startServer(self):
        start_channel = 0
        serverfnc.clear_logs()
        std.wait_clear()

        print(colored("How many channels do you want to run? (1-8)", "green"))
        input(colored(">> ", "green"))

        try:
            start_channel = int(input(f"How many channels do you want to run? (1-8)\n>> "))
        except ValueError:
            print(colored("INVALID INPUT. EXITING!", "red"))
            std.wait_clear()
            std.exit_menu()

        if start_channel < 1 or start_channel > 8:
            print(colored("INVALID INPUT. EXITING!", "red"))
            std.wait_clear()
            std.exit_menu()

        def run_command(command, log_file):
            with open(log_file, "a") as f:
                subprocess.Popen(command, stdout=f, stderr=subprocess.STDOUT, shell=True)
            time.sleep(0.5)

        print(colored("Starting on DB", "magenta"))
        run_command(config["server"][0]["xsf_db"], "_tmp/start_db.log")

        # Uruchamianie serwera autoryzacji
        print(colored("Starting on Auth", "magenta"))
        run_command(config["server"][0]["xsf_auth"], "_tmp/start_auth.log")

        # Uruchamianie kanałów
        for ch in range(1, start_channel + 1):
            channel_path = config["server"][0]["xsf_channel"] + f"/ch{ch}"
            pchannel_path = config["server"][0]["xsf_channel"] + f"/ch{ch}/pch{ch}"

            run_command(f"{channel_path}", f"_tmp/start_ch{ch}.log")
            run_command(f"{pchannel_path}", f"_tmp/start_pch{ch}.log")
            print(colored(f"Starting on CH/pCH{ch}", "magenta"))

        # Uruchamianie kanału 99
        print(colored("Starting on Ch99", "magenta"))
        run_command(config["server"][0]["xsf_special_channel"], "_tmp/start_ch99.log")

    def stopServer(self, service_path, service_name):
        print(colored(f"Stopping {service_name}", "yellow"))
        subprocess.run(service_path, shell=True)
        pid_file = Path("./pid")
        if pid_file.exists() and pid_file.is_file() and pid_file.is_readable():
            with pid_file.open() as f:
                pid = f.read().strip()
            subprocess.run(["kill", "-1", pid], check=True)
            time.sleep(0.5)

        self.stopServer(config["server"][0]["xsf_db"], "DB")
        self.stopServer(config["server"][0]["xsf_auth"], "Auth")

        for off_ch in range(1, 9):
            channel_path = config["server"][0]["xsf_channel"] + f"/ch{off_ch}"
            pchannel_path = config["server"][0]["xsf_channel"] + f"/ch{off_ch}/pch{off_ch}"

            self.stopServer(channel_path, f"Ch{off_ch}")
            self.stopServer(pchannel_path, f"pCh{off_ch}")

        self.stopServer(config["server"][0]["xsf_special_channel"], "Ch99")
