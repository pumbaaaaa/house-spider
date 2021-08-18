import configparser
import random
import time

from common.util.html import get_html
from source.data import Data


def lj_spider(config, data):
    # 获取地址
    lj_area = config.get('website', 'lj_area')
    url = config.get('website', 'lj')

    for area in lj_area.split(','):
        # 区域Url格式化
        req_url = config.get('website', 'req_lj').format(area)
        # 爬取数据
        html = get_html(req_url)
        # 保存数据，获取最大页码
        max_page = data.lj_save(html, url, req_url, True)

        # 大于1页，遍历爬取
        for i in range(max_page + 1):
            if i > 1:
                req_url_pg = config.get('website', 'req_lj_pg').format(area, str(i))
                html = get_html(req_url_pg)
                data.lj_save(html, url, req_url, False)

        # 暂停时间，模拟人工操作
        time.sleep(random.randint(1, 10))


def bk_spider(config, data):
    bk_area = config.get('website', 'bk_area')
    url = config.get('website', 'bk')

    for area in bk_area.split(','):
        req_url = config.get('website', 'req_bk').format(area)
        html = get_html(req_url)
        max_page = data.bk_save(html, url, req_url, True)

        for i in range(max_page + 1):
            if i > 1:
                req_url_pg = config.get('website', 'req_bk_pg').format(area, str(i))
                html = get_html(req_url_pg)
                data.bk_save(html, url, req_url, False)

        time.sleep(random.randint(1, 10))


if __name__ == '__main__':
    print('Spider-Man!!')

    # 获取配置
    config = configparser.ConfigParser()
    config.read("config.ini")

    # 获取数据源
    data = Data(config)

    lj_spider(config, data)
    bk_spider(config, data)
