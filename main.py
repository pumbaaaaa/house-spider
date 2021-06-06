import configparser
import random
import time
from source.data import Data
from common.util.html import get_html

if __name__ == '__main__':
    print('Spider-Man!!')

    config = configparser.ConfigParser()
    config.read("config.ini")

    data = Data(config)
    conn = data.get_connection()

    lj_area = config.get('website', 'lj_area')
    url = config.get('website', 'lj')
    for area in lj_area.split(','):
        req_url = config.get('website', 'req_lj').format(area)
        html = get_html(url)
        data.lj_save(html, url, req_url)
        time.sleep(random.randint(1, 20))
