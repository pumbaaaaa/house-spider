from html.parser import HTMLParser


class LianJiaParser(HTMLParser):

    def __init__(self, url, req_url, is_first_page):
        super().__init__()
        self.url = url
        self.req_url = req_url
        self.span = ""
        self.houseName = []
        self.villageName = []
        self.houseNote = []
        self.houseNoteTmp = ""
        self.houseTotalPrice = []
        self.houseUnitPrice = []
        self.houseAge = []
        self.houseArea = ""
        self.houseSquare = []
        self.houseLink = []
        self.houseImg = []
        self.flag = []
        self.maxPage = 1
        self.is_first_page = is_first_page

    def feed(self, data):
        super().feed(data)

        return self.houseName, self.villageName, self.houseNote, self.houseTotalPrice, self.houseUnitPrice, self.houseAge, self.houseArea, self.houseSquare, self.houseLink, self.houseImg, self.maxPage

    def handle_starttag(self, tag, attrs):
        if tag == "span":
            self.flag.append("span")
        elif tag == 'a' and "data-page" in [x[0] for x in attrs] and self.is_first_page:
            # 分页
            self.flag.append("page")
        elif tag == 'a' and ("href", self.req_url[len(self.url):]) in attrs and ("class", "selected") in attrs:
            # 区域
            self.flag.append("houseArea")
        elif tag == "a" and ("data-el", "ershoufang") in attrs and ("class", "title") in attrs:
            # 简介
            self.flag.append("houseName")
            for attr in attrs:
                if attr[0] == "href":
                    self.houseLink.append(attr[1])
        elif tag == "a" and ("data-el", "region") in attrs:
            # 小区
            self.flag.append("villageName")
        elif tag == "div" and ("class", "houseInfo") in attrs:
            # 说明
            self.flag.append("houseNote")
        elif tag == "div" and ("class", "totalPrice") in attrs:
            # 总价
            self.flag.append("houseTotalPrice")
        elif tag == "div" and ("class", "unitPrice") in attrs:
            # 单价
            self.flag.append("houseUnitPrice")
        elif tag == "img" and ("class", "lj-lazy") in attrs:
            # 图片连接
            for attr in attrs:
                if attr[0] == "alt":
                    for attr2 in attrs:
                        if attr2[0] == "data-original":
                            self.houseImg.append(attr2[1])
                            break
                    break

    def handle_data(self, data):
        data = data.replace(' ', '')
        if len(self.flag) > 0:
            if self.flag[-1] == "span":
                # print(str(data))
                self.span = data
                self.flag.pop()
                if len(self.flag) > 0 and self.flag[-1] == "houseUnitPrice":
                    self.houseUnitPrice.append(self.span)
                    self.flag.pop()
            elif self.flag[-1] == "page":
                if self.maxPage < int(data):
                    self.maxPage = int(data)
                self.flag.pop()
            elif self.flag[-1] == "houseArea":
                self.houseArea = data
                self.flag.pop()
            elif self.flag[-1] == "houseName":
                # print(str(data))
                self.houseName.append(data)
                self.flag.pop()
            elif self.flag[-1] == "villageName":
                # print(str(data))
                self.villageName.append(data)
                self.flag.pop()
            elif self.flag[-1] == "houseTotalPrice":
                # print(str(data))
                self.houseTotalPrice.append(self.span + data)
                self.span = ""
                self.flag.pop()
            if len(self.flag) > 0 and self.flag[-1] == "houseNote":
                # print(str(data))
                self.houseNoteTmp = self.houseNoteTmp + data
                for s in str(data).split("|"):
                    if "平米" in s:
                        self.houseSquare.append(s)
                    elif "年建" in s:
                        self.houseAge.append(s)

    def handle_endtag(self, tag):
        if tag == "div" and len(self.flag) > 0 and self.flag[-1] == "houseNote":
            self.houseNote.append(self.houseNoteTmp)
            self.houseNoteTmp = ""
            self.flag.pop()

    def error(self, message):
        print('========Parser failed==========')
        pass
