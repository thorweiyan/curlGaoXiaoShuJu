# -*- coding: utf-8 -*-

import detail
import writeTxt
import time

if __name__ == '__main__':

    prefix_url = 'https://www.topuniversities.com'
    all_url = 'https://www.topuniversities.com/sites/default/files/qs-rankings-data/914824.txt?_=1561021794824'
    web_list = detail.curl_list(all_url)
    writeTxt.open_txt()

    index = 0
    for web in web_list:
        # 从上次出错的地方开始爬
        if index < 910:
            index += 1
            continue

        try:
            print("index", index)
            index += 1
            url = prefix_url + web['url']
            print("title", web['title'])
            print("url", url)
            time.sleep(2)
            data_list = detail.curl_detail(url)
            # 名字里带逗号的改成空格
            title = web['title'].replace(',', ' ')
            # 名字里带中文引号的改成英文的
            title = title.replace('’', '\'')
            # 名字里带中文减号的改成英文的
            title = title.replace('–', '-')
            title = title.replace('ń', 'n')
            print("title", title)
            data_list.insert(0, title)
            writeTxt.write_to_txt(data_list)
        except:
            # 不管怎样，先关闭txt才能保存之前成果
            print('error')
            writeTxt.close_txt()

    writeTxt.close_txt()
