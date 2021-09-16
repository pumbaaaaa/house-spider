from html.parser import HTMLParser
from ast import literal_eval


class BeiKeParser(HTMLParser):

    def __init__(self, url, req_url, is_first_page):
        super().__init__()
        self.url = url
        self.req_url = req_url
        self.span = ""
        self.houseName = []
        self.villageName = []
        self.houseNote = []
        self.houseTotalPrice = []
        self.houseTotalPrice_tmp = ""
        self.houseUnitPrice = []
        self.houseAge = []
        self.houseArea = ""
        self.houseSquare = []
        self.houseLink = []
        self.houseImg = []
        self.flag = []
        self.maxPage = 1
        self.is_first_page = is_first_page
        self.sign = 0

    def feed(self, data):
        super().feed(data)

        return self.houseName, self.villageName, self.houseNote, self.houseTotalPrice, self.houseUnitPrice, self.houseAge, self.houseArea, self.houseSquare, self.houseLink, self.houseImg, self.maxPage

    def handle_starttag(self, tag, attrs):
        if tag == "span":
            if ("class", "houseIcon") in attrs:
                self.flag.append("houseNote")
            self.flag.append("span")
        elif tag == 'div' and "page-data" in [x[0] for x in attrs] and self.is_first_page:
            # print(tag, attrs)
            self.maxPage = literal_eval(str(attrs[3][1]))['totalPage']
        elif tag == 'a' and ("href", self.req_url[len(self.url):]) in attrs and ("class", "selected CLICKDATA") in attrs:
            self.flag.append("houseArea")
        elif tag == "a" and ("class", "img VIEWDATA CLICKDATA maidian-detail") in attrs:
            # self.flag.append("houseName")
            for attr in attrs:
                if attr[0] == "title":
                    self.houseName.append(attr[1])
                elif attr[0] == "href":
                    self.houseLink.append(attr[1])
        elif tag == "div" and ("class", "totalPrice totalPrice2") in attrs:
            self.flag.append("houseTotalPrice_2")
        elif tag == "div" and ("class", "unitPrice") in attrs:
            self.flag.append("houseUnitPrice_2")
        elif tag == "img" and ("class", "lj-lazy") in attrs:
            for attr in attrs:
                if attr[0] == "alt":
                    for attr2 in attrs:
                        if attr2[0] == "data-original":
                            self.houseImg.append(attr2[1])
                            break
                    break
        elif tag == "div" and ("class", "positionInfo") in attrs:
            self.flag.append("villageName_1")
        elif tag == "a" and len(self.flag) > 0 and self.flag[-1] == "villageName_1":
            self.flag.pop()
            self.flag.append("villageName_2")

    def handle_data(self, data):
        data = data.replace(' ', '')
        if len(self.flag) > 0:
            if self.flag[-1] == "span":
                self.span = data
                self.flag.pop()
                if len(self.flag) > 0 and self.flag[-1] == "houseUnitPrice_2":
                    self.houseUnitPrice.append(self.span)
                    self.flag.pop()
                elif len(self.flag) > 0 and self.flag[-1] == "houseNote":
                    self.houseNote.append(self.span)
                    for s in str(data).split("|"):
                        if "平米" in s:
                            self.houseSquare.append(s)
                        elif "年建" in s:
                            self.houseAge.append(s)
                    self.flag.pop()
            elif self.flag[-1] == "houseArea":
                self.houseArea = data
                self.flag.pop()
            elif self.flag[-1] == "houseName":
                # print(str(data))
                self.houseName.append(data)
                self.flag.pop()
            elif self.flag[-1] == "houseTotalPrice_2":
                if data != "":
                    self.houseTotalPrice_tmp = self.houseTotalPrice_tmp + self.span + data
                self.span = ""
                # self.flag.pop()
            elif self.flag[-1] == "villageName_2":
                # print(str(data))
                self.villageName.append(data)
                self.flag.pop()

    def handle_endtag(self, tag):
        if tag == "div" and len(self.flag) > 0 and self.flag[-1] == "houseTotalPrice_2":
            self.houseTotalPrice.append(self.houseTotalPrice_tmp)  # .replace(' ', ''))
            self.houseTotalPrice_tmp = ""
            self.flag.pop()

    def error(self, message):
        print('========Parser failed==========')
        pass
