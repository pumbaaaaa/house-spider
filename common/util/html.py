import random
import urllib.request


def get_html(url):
    user_agents = [
        'User-Agent:Mozilla/5.0',
        'User-Agent:Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36',
        'User-Agent:Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36',
        'User-Agent:Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
    ]
    agent = random.choice(user_agents)
    headers = {'User-Agent': agent}
    req = urllib.request.Request(url, headers=headers)
    page = urllib.request.urlopen(req)  # urllib.urlopen()方法用于打开一个URL地址
    html = page.read()  # read()方法用于读取URL上的数据
    return html.decode('UTF-8').replace(u'\xa9', u'').replace("'", "").replace("\r\n", "").replace("\n", "")
