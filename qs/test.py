# -*- coding: utf-8 -*-

import detail
import writeTxt

if __name__ == '__main__':
    url1 = 'https://www.topuniversities.com/universities/massachusetts-institute-technology-mit#wurs'
    list = detail.curl_detail(url1)
    writeTxt.open_txt()
    writeTxt.write_to_txt(list)
    writeTxt.close_txt()

    # url2 = 'https://www.topuniversities.com/sites/default/files/qs-rankings-data/914824.txt?_=1561021794824'
    # detail.curl_list(url2)
