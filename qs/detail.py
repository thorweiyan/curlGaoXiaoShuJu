# -*- coding: utf-8 -*-
# 查询详情，返回需要的数据
import requests
import re
import json

# 一般是这样的，例如第一个例子中的：
# <div class="rank tab-pane fees" id="data">
# <div class="student line"><div class="set">
# <h4>Total students - 11,145</h4>
# <div class="fee"><label>PG students</label><div> 60%</div></div>
# <div class="fee"><label>UG students</label><div> 40%</div></div>
# </div>
# <div class="set"><h4>International students - 3,732</h4>
# <div class="fee"><label>UG students</label><div> 17%</div></div>
# <div class="fee"><label>PG students</label><div> 83%</div></div></div></div>
# <div class="faculty"><div class="set"><h4>Total faculty staff - 3,009</h4>
# <div class="fee"><label>Domestic staff</label><div> 1313</div></div>
# <div class="fee"><label>International staff</label><div> 1696</div></div></div></div></div>

pattern1 = 'class="rank tab-pane fees" id="data"(.*?)</div></div></div></div></div>'


def curl_detail(url):
    web = requests.get(url)
    try:
        text = re.findall(pattern1, web.text)[0]
    except:
        return ['null'] * 9
    # print(text)
    # 存储所有的数据
    list = []
    try:
        list.append(re.findall('Total students - (.*?)<', text)[0])
    except:
        list.append('null')
    try:
        list.append(re.findall('PG students</label><div> (.*?)<', text)[0])
    except:
        list.append('null')
    try:
        list.append(re.findall('UG students</label><div> (.*?)<', text)[0])
    except:
        list.append('null')
    try:
        list.append(re.findall('International students - (.*?)<', text)[0])
    except:
        list.append('null')
    try:
        list.append(re.findall('UG students</label><div> (.*?)<', text)[1])
    except:
        list.append('null')
    try:
        list.append(re.findall('PG students</label><div> (.*?)<', text)[1])
    except:
        list.append('null')
    try:
        list.append(re.findall('Total faculty staff - (.*?)<', text)[0])
    except:
        list.append('null')
    try:
        list.append(re.findall('Domestic staff</label><div> (.*?)<', text)[0])
    except:
        list.append('null')
    try:
        list.append(re.findall('International staff</label><div> (.*)', text)[0])
    except:
        list.append('null')

    for index in range(len(list)):
        temp = ''.join(list[index].split(','))
        list[index] = temp
    # print(list)
    return list


def curl_list(url):
    web = requests.get(url)
    # print(web.text)
    all_website = json.loads(web.text)['data']
    # web_list = []
    # for website in all_website:
    #     web_list.append(website['url'])
    return all_website
