
from prettytable import PrettyTable

# sys.setdefaultencoding('utf8')

def init_dict_from_list(l: list):
    return dict.fromkeys(
        [arr[1].title() for arr in l], 0,
    )

# UNUSELESS
def get_pretty_table(headers: list, data: list):
    table = PrettyTable()
    for i, header in enumerate(headers):
        table.add_column(
            header, 
            data[i],
            align="c"
        )
    return table

def fcost(cost: int) -> str:
    return "₽ {0:,}".format(cost)

def fnotes(notes: dict) -> str:
    response = "\n".join(
            [f"{category}{'..' * (15 - len(str(cost)))}{fcost(cost)}" \
                for category, cost in notes.items()])
    response += "\n" + "="*18 + "\n" + \
            f"Всего: {fcost(sum(list(notes.values())))}"
    return response