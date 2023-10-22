from os import getcwd, listdir, environ

global DB
if ".env" in listdir(getcwd()):
    from dotenv import load_dotenv

    DB = dict()

    load_dotenv(f"{getcwd()}/.env")

    # Access the variables
    DB["port"] = environ.get("DB_PORT")
    DB["name"] = environ.get("DB_NAME")
    DB["host"] = environ.get("DB_HOST")
    DB["pass"] = environ.get("DB_PASS")
    DB["user"] = environ.get("DB_USER")
else:
    raise FileNotFoundError(f".env not found")


def list():
    for key in DB:
        print(DB[key])
