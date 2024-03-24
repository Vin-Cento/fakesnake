from os import listdir, path
import platform

from dotenv import dotenv_values


def utils_getDB():
    DB = dict()
    if platform.system() == "Linux":
        folder = f"{path.expanduser('~')}/.config/fakesnake"
        if ".env" in listdir(folder):
            v = dotenv_values(f"{folder}/.env")

            for e in v.keys():
                DB[e] = v[e]
        else:
            print(
                f"""
            Missing .env
            Run: fakes db init
            """
            )
        return DB
    else:
        print("only available on linux")
        exit()
