# from prettytable import PrettyTable

# sys.setdefaultencoding('utf8')

def init_dict_from_list(l: list):
    return dict.fromkeys(
        [arr[1].title() for arr in l], 0,
    )

# # UNUSELESS
# def get_pretty_table(headers: list, data: list):
#     table = PrettyTable()
#     for i, header in enumerate(headers):
#         table.add_column(
#             header, 
#             data[i],
#             align="c"
#         )
#     return table

def fcost(cost: int) -> str:
    return "₽ {0:,}".format(cost)

def fother(other) -> str:
    apd = 15

    if len(other) > apd:
        return f"{other[:apd]}.."
    elif len(other) in [3,5] or "о" in other.lower():
        
        return f"{other}{'. '*(apd+2-len(other))}"
    else:
        return f"{other}{'. '*(apd+1-len(other))}"

def fnotes(notes: dict) -> str:
    response = "\n".join(
            [f"{fother(category)} {fcost(cost)}" \
                for category, cost in notes.items()])
    response += "\n" + "="*18 + "\n" + \
            f"Всего: {fcost(sum(list(notes.values())))}"
    return response
