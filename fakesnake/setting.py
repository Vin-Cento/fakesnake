from os import getcwd, listdir, environ

global DB
from dotenv import load_dotenv

DB = dict()

if ".env" in listdir(getcwd()):
    load_dotenv(f"{getcwd()}/.env")

    # Access the variables
    DB["port"] = environ.get("DB_PORT")
    DB["name"] = environ.get("DB_NAME")
    DB["host"] = environ.get("DB_HOST")
    DB["pass"] = environ.get("DB_PASS")
    DB["user"] = environ.get("DB_USER")
else:
    DB["port"] = "5432"
    DB["name"] = "postgres"
    DB["host"] = "localhost"
    DB["pass"] = ""
    DB["user"] = "postgres"


def list():
    for key in DB:
        print(DB[key])
