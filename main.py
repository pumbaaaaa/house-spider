import configparser
import random
import time
from source.data import Data
from common.util.html import get_html

if __name__ == '__main__':
    print('Spider-Man!!')

    # 获取配置
    config = configparser.ConfigParser()
    config.read("config.ini")

    # 获取数据源
    data = Data(config)
    conn = data.get_connection()

    # 获取地址
    lj_area = config.get('website', 'lj_area')
    url = config.get('website', 'lj')

    for area in lj_area.split(','):
        # 区域Url格式化
        req_url = config.get('website', 'req_lj').format(area)
        # 爬取数据
        html = get_html(req_url)
        # 保存数据，获取最大页码
        maxPage = data.lj_save(html, url, req_url, True)

        # 大于1页，遍历爬取
        for i in range(maxPage + 1):
            if i > 1:
                req_url_pg = config.get('website', 'req_lj_pg').format(area, str(i))
                html = get_html(req_url_pg)
                data.lj_save(html, url, req_url, False)

                # 暂停时间，模拟人工操作
                time.sleep(random.randint(1, 10))

        # 暂停时间，模拟人工操作
        time.sleep(random.randint(1, 10))
