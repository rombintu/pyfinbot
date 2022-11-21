from pycbrf.toolbox import ExchangeRates
from datetime import datetime

def convert_to_rub(usd) -> int:
    today = datetime.today().strftime("%Y-%m-%d")
    rates = ExchangeRates(today)
    return int(usd * rates["USD"].value)

def convert_to_int(arg: str) -> int:
    try:
        return int(arg)
    except ValueError:
        return -1

def find_K_in_int(arg: str) -> int:
    if arg[-1] == "$":
        if arg[-2].lower() in ["к","k"]:
            return convert_to_rub(convert_to_int(arg[:-2])) * 1000
        return convert_to_rub(convert_to_int(arg[:-1]))
    else:
        if arg[-1].lower() in ["к","k"]:
            return convert_to_int(arg[:-1]) * 1000
        return convert_to_int(arg)

def filter_by_input(text: str):
    note = {
        "cost": -1,
        "category": "",
        "comment": "",
    }
    args = text.split(" ")
    if len(args) >= 2:
        note["cost"] = find_K_in_int(args[0])
        note["category"] = args[1].lower()
        note["comment"] = " ".join(args[2:]) or ""
    return note
    
    