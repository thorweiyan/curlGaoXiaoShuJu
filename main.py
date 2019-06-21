# -*- coding: utf-8 -*-
import login
from time import sleep

db_name = "test.db"


def main():
    log = login.Curl_data
    # 设置登录信息
    log.set_login_data(log, "syjiang@zju.edu.cn", "e10adc3949ba59abbe56e057f20f883e")

    # 模拟登录
    if not log.login(log):
        print("error on login!")
        return

    # # 模拟获得第一版菜单（核心指标），即type为"0"
    # status, menu = log.get_menus(log, "0")
    # if not status:
    #     print("error in get_menus!")
    #     return

    # # 根据返回的menu，获取具体数据并存放到db中
    # if not log.circular_get_data_db(log, menu):
    #     print("error in get_data0!")
    #     return
    
    # sleep(60)

    # 模拟获得第二版菜单（省级指标），即type为"1"
    status, menu = log.get_menus(log, "1")
    if not status:
        print("error in get_menus!")
        return

    # 根据返回的menu，获取具体数据并存放到db中
    if not log.circular_get_data_db(log, menu):
        print("error in get_data1!")
        return


if __name__ == "__main__":
    main()
