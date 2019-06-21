# -*- coding: utf-8 -*-
import sqlite3
import json

conn_dict = {}


def saveItem(db_name, table_name, data):
    if not is_exists(db_name):
        return False
    conn = conn_dict[db_name]
    cursor = conn.cursor()

    ins = (
        "INSERT OR REPLACE INTO "
        + table_name
        + " values ("
        + "?," * len(data[0]["linedata"])
    )
    ins = ins[:-1] + ")"
    for dd in data:
        v = tuple(dd["linedata"])
        cursor.execute(ins, v)
    cursor.close()
    conn.commit()
    print("Save data successfully")
    return True


def open_db(db_name):
    conn = sqlite3.connect(db_name)
    conn.text_factory = str
    conn_dict[db_name] = conn
    print("Opened database successfully")


def close_db(db_name):
    if db_name in conn_dict:
        conn_dict[db_name].commit()
        conn_dict[db_name].close()
        conn_dict.pop(db_name)
    print("Close database successfully")


def is_exists(db_name):
    if db_name in conn_dict:
        return True
    print("db isn't exists!")
    return False


def create_table(db_name, table_name, columns):
    if not is_exists(db_name):
        return False

    sql = "CREATE TABLE " + table_name + "("
    ins = "INSERT OR REPLACE INTO " + table_name + " values (" + "?," * len(columns)
    ins = ins[:-1] + ")"

    l = ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten", "eleven", "twelve", "thirteen", "fourteen", "fifteen", "sixteen", "seventeen", "eighteen", "ninteen", "twenty"]
    index = 0
    v = []
    for column in columns:
        sql += l[index] + " TEXT,"
        # sql += column['label'] + ' TEXT,'
        v.append(column["label"])
        index += 1
    sql = sql[:-1] + ");"

    conn = conn_dict[db_name]
    c = conn.cursor()
    print(sql)
    try:
        c.execute(sql)
    except sqlite3.OperationalError as identifier:
        print("table exists")
        return False
    else:
        print(ins)
        c.execute(ins, tuple(v))
        conn.commit()
        print("Table created successfully")
    return True


# 测试
if __name__ == "__main__":
    db_name = "test.db"
    table_name = "测试双一流"
    with open("./test_columns.json", "rb") as f:
        columns = json.loads(f.read().decode("utf-8"))

        print("加载入文件完成...")
        print(columns)

    with open("./test_data.json", "rb") as f:
        # data = json.loads(f.read().decode('gbk', 'ignore').encode('utf-8'))
        data = json.loads(f.read().decode("utf-8"))
        # data = json.dumps(temp)
        print("加载入文件完成...")
        print(data)

    print(columns)
    open_db(db_name)
    create_table(db_name, table_name, columns)
    saveItem(db_name, table_name, data)
    close_db(db_name)

