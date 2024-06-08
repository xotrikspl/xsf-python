from termcolor import colored
from menu.server import serverMenu
from menu.backup import backupMenu
import menu.standard as std


def mainMenu():
    std.wait_clear()
    print(colored('Main Menu', 'green'))
    menu = {
        "1": ("Server", serverMenu),
        "2": ("Backup", backupMenu),
        # "3": ("Compile", compileMenu),
        # "4": ("Server Installation", installMenu),
        # "5": ("Tools", toolsMenu),
        # "h": ("Help menu", helpMenu),
        "q": ("Exit", std.exit_menu)
    }

    for menuKey in sorted(menu.keys()):
        print(menuKey + colored(" -> ", "green") + menu[menuKey][0])

    selectMenu = input(colored(">> ", "green"))
    menu.get(selectMenu, [None, std.Invalid])[1]()


if __name__ == "__main__":
    mainMenu()
