import os, sys
from dotenv import load_dotenv

# load vars from .env file
load_dotenv()

error_parse = "Some vars from .env is None: {}"

def parse_dotenv() -> dict:
    envs = {
        "TOKEN" : os.getenv('TOKEN', default=None),
        "DATABASE" : os.getenv("DATABASE", default="sqlite://"),
        # "DEVMODE": os.getenv("DEVMODE", default=True),
    }
    if None in envs.values():
        print(error_parse.format(["TOKEN, DATABASE"]))
        sys.exit(0)
    return envs