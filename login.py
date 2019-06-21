# -*- coding: utf-8 -*-
import requests
import sql
from time import sleep
import random


class Curl_data:
    data = {}
    data["ct"] = ""
    login_url = "https://beta.cingta.com/users/mylogin/"
    get_menus_url = "https://beta.cingta.com/basedata/get_menus/"
    get_maindata_url = "https://beta.cingta.com/basedata/get_maindata/"
    get_countdata_url = "https://beta.cingta.com/basedata/get_countdata/"
    userid = 0
    main_cookies = None
    post_data = {}
    post_data["entity"] = []
    post_data["onlySchool"] = False
    post_data["pageSize"] = 20

    # 模拟登录
    def login(self):
        main_html = requests.post(self.login_url, data=self.data)
        if main_html.status_code != 200:
            return False
        self.main_cookies = main_html.cookies
        print(main_html.json())
        self.userid = main_html.json()["data"]["id"]
        return True

    # 获得菜单
    def get_menus(self, typ):
        menus = requests.post(
            self.get_menus_url,
            json={"type": typ, "userid": self.userid},
            cookies=self.main_cookies,
        )
        if menus.status_code != 200:
            return False, None
        return True, menus.json()

    # 设置登录信息
    def set_login_data(self, user_name, password):
        self.data["password"] = password
        self.data["username"] = user_name

    # 循环获取数据并存储
    def circular_get_data_db(self, menu):
        # 跳过前面多少个
        index = 1
        c = 1
        for cur in menu["data"]:
            if c < index:
                c += 1
                continue
            db_name = cur["label"] + ".db"
            print("managing database: " + db_name)
            sql.open_db(db_name)
            if self.circular_get_data_table(self, db_name, cur["children"]):
                sql.close_db(db_name)
            else:
                print("circular_get_data_db error: " + db_name)
                return False
        return True

    def circular_get_data_table(self, db_name, tables):
        # 跳过前面多少个
        index = 1
        cur = 1
        for table in tables:
            if cur < index:
                cur += 1
                continue
            table_name_origin = table["label"]
            print(
                "managing table: name:"
                + table_name_origin
                + " id : "
                + str(table["id"])
            )
            # 获取统计数据和明细数据
            urls = [self.get_maindata_url, self.get_countdata_url]
            table_name_lastfix = ["明细", "统计"]
            for index in [0, 1]:
                # 10 +- 3秒
                sleep_time = 7+random.random()*6
                print("sleep for:" + str(sleep_time))
                sleep(sleep_time)

                url = urls[index]
                table_name = table_name_origin + table_name_lastfix[index]

                # 获取表头
                status, columns = self.get_columns(self, table["id"], url)
                if not status:
                    print("no columns?")
                    continue
                    # return False

                # 新建数据表
                if not sql.create_table(db_name, table_name, columns):
                    print(
                        "circular_get_data_table create_table error: db_name: "
                        + db_name
                        + " table_name:"
                        + table_name
                    )
                    continue
                
                # 爬取数据并写入
                # 本次只需要表头
                # status, data = self.circular_get_data(self, table["id"], url)
                # if status:
                #     if not self.save_data(self, db_name, table_name, data):
                #         return False
                # else:
                #     print("circular_get_data_table error: " + table_name)
                #     return False
        return True

    def save_data(self, db_name, table_name, data):
        if not sql.saveItem(db_name, table_name, data):
            print(
                "save data saveItem error: db_name: "
                + db_name
                + " table_name:"
                + table_name
            )
            return False
        return True

    # 按照page分页获取数据，注意sleep时间
    def circular_get_data(self, indexid, url):
        self.post_data["indexid"] = str(indexid)
        self.post_data["userid"] = self.userid

        index = 1
        data = []
        while True:
            print("getting the " + str(index) + "page.......")
            self.post_data["pageNo"] = index
            index += 1

            mc_data = requests.post(url, json=self.post_data, cookies=self.main_cookies)
            if mc_data.status_code != 200:
                print("get main data error!")
                return False, None
            mc_data = mc_data.json()
            if len(mc_data["data"]["table"]) == 0:
                break
            data += mc_data["data"]["table"]
            # 10 +- 3秒
            sleep(7+random.random()*6)

        return True, data

    # 获取表头
    def get_columns(self, indexid, url):
        self.post_data["indexid"] = str(indexid)
        self.post_data["userid"] = self.userid

        columns = []
        self.post_data["pageNo"] = 1

        mc_data = requests.post(url, json=self.post_data, cookies=self.main_cookies)
        if mc_data.status_code != 200:
            print("get main/count data error!")
            return False, None
        mc_data = mc_data.json()
        columns = mc_data["data"]["columnData"]

        return True, columns
