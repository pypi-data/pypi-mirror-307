from not1mm.lib.database import DataBase
from json import loads
import not1mm.fsutils as fsutils
import os

dbname = None
pref = {}


def load_pref():
    try:
        if os.path.exists(fsutils.CONFIG_FILE):
            with open(fsutils.CONFIG_FILE, "rt", encoding="utf-8") as file_descriptor:
                pref = loads(file_descriptor.read())
        else:
            pref["current_database"] = "ham.db"

    except IOError:
        ...


load_pref()
dbname = fsutils.USER_DATA_PATH / pref.get("current_database", "ham.db")
database = DataBase(dbname, fsutils.USER_DATA_PATH)

database.create_callhistory_table()
database.delete_callhistory()

try:
    with open(
        "/home/mbridak/call_history/CWOPS_3634-AAA.txt", "rt", encoding="utf-8"
    ) as file_descriptor:
        lines = file_descriptor.readlines()
        if "!!Order!!" in lines[0]:
            item_names = lines[0].strip().split(",")
            # ['!!Order!!', 'Call', 'Sect', 'State', 'CK', 'UserText', '']
            item_names = item_names[1:-1]
            # ['Call', 'Sect', 'State', 'CK', 'UserText']
            lines = lines[1:]
            group_list = []
            for line in lines:
                if line.startswith("#"):
                    continue
                group = {}
                fields = line.strip().split(",")
                # ['4U1WB','MDC','DC','89','']
                count = 0
                try:
                    for item in item_names:
                        if item == "":
                            continue
                        group[item] = fields[count]
                        count += 1
                    group_list.append(group)
                    # database.add_callhistory_item(group)
                    # print(f"{group=}")
                except IndexError:
                    ...
            database.add_callhistory_items(group_list)
except FileNotFoundError:
    print("error")
