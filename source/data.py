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

    def lj_save(self, html, url, req_url):
        lj = LianJiaParser(url, req_url)

        houseName, villageName, houseNote, houseTotalPrice, houseUnitPrice, houseAge, houseArea, houseSquare, houseLink, houseImg = lj.feed(
            html)
        for j in range(len(houseName)):
            print(houseName[j], villageName[j], houseNote[j], houseTotalPrice[j], houseUnitPrice[j], houseAge[j],
                  houseArea[j], houseSquare[j], houseLink[j], houseImg[j])

    def save_mysql(self, webName, houseName, villageName, houseNote, houseTotalPrice, houseUnitPrice, houseAge,
                   houseArea, houseSquare, houseLink, houseImg):
        insert_sql = """insert into {}(webName, houseName, villageName, houseNote, houseTotalPrice, houseUnitPrice, 
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
        print(webName + 'saved' + str(saved_rows) + 'rows')
        conn.commit()
        cursor.close()
        conn.close()
