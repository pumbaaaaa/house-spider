from .beike import BeiKeParser
from .lianjia import LianJiaParser


class Data:

    def __init__(self, config):
        self._config = config
        pass

    def get_connection(self):
        import pymysql

        host = self._config.get('mysql', 'host')
        port = self._config.getint('mysql', 'port')
        user = self._config.get('mysql', 'user')
        passwd = self._config.get('mysql', 'passwd')
        db = self._config.get('mysql', 'db')

        conn = pymysql.connect(host=host, port=port, user=user, password=passwd, db=db, charset='utf8')
        return conn

    def lj_save(self, html, url, req_url, first_page_flag):
        print(req_url)
        lj = LianJiaParser(url, req_url, first_page_flag)

        houseName, villageName, houseNote, houseTotalPrice, houseUnitPrice, houseAge, houseArea, houseSquare, houseLink, houseImg, maxPage = lj.feed(
            html)

        self.save_mysql('链家', houseName, villageName, houseNote, houseTotalPrice, houseUnitPrice, houseAge, houseArea,
                        houseSquare, houseLink, houseImg)
        return maxPage

    def bk_save(self, html, url, req_url, first_page_flag):
        print(req_url)
        bk = BeiKeParser(url, req_url, first_page_flag)

        houseName, villageName, houseNote, houseTotalPrice, houseUnitPrice, houseAge, houseArea, houseSquare, houseLink, houseImg, maxPage = bk.feed(
            html)

        self.save_mysql('贝壳', houseName, villageName, houseNote, houseTotalPrice, houseUnitPrice, houseAge, houseArea,
                        houseSquare, houseLink, houseImg)

        return maxPage

    def save_mysql(self, webName, houseName, villageName, houseNote, houseTotalPrice, houseUnitPrice, houseAge,
                   houseArea, houseSquare, houseLink, houseImg):
        insert_sql = """insert ignore into {}(webName, houseName, villageName, houseNote, houseTotalPrice, houseUnitPrice, 
        houseAge, houseArea, houseSquare, houseLink, houseImg) values""".format(
            "t_house")
        conn = self.get_connection()
        cursor = conn.cursor()

        for i in range(len(houseName)):
            if i == 0:
                insert_sql += """('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}')""" \
                    .format(webName, houseName[i], villageName[i], houseNote[i], houseTotalPrice[i],
                            houseUnitPrice[i], houseAge[i], houseArea, houseSquare[i], houseLink[i], houseImg[i])
            else:
                insert_sql += """,('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}')""" \
                    .format(webName, houseName[i], villageName[i], houseNote[i], houseTotalPrice[i],
                            houseUnitPrice[i], houseAge[i], houseArea, houseSquare[i], houseLink[i], houseImg[i])
        insert_sql += """;"""
        saved_rows = 0
        if len(houseName) > 0:
            saved_rows = cursor.execute(insert_sql)
        print(webName + ' saved ' + str(saved_rows) + ' rows')
        conn.commit()
        cursor.close()
        conn.close()
