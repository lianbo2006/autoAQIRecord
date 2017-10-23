#classDef.py

from pymongo import MongoClient
from datetime import datetime
from bs4 import BeautifulSoup
from pprint import pprint
import requests

class mongoType():
    #定义数据类，参数有地址（client），数据库（db），集合（col）
    def __init__(self):
        self.client = MongoClient('219.216.87.8', 27017)
        self.db = self.client["aqi_record"]
        #集合以时间命名，xxxx-xx-xx
        self.col = self.db[datetime.now().strftime("%Y-%m-%d")]


    def dicWrite(self, iDic):
        #向数据库写入单条数据，数据为字典
        self.col.insert_one(iDic)

    def dicListWrite(self, iDicList):
        #向数据库写入多条数据，数据为字典列表
        self.col.insert_many(iDicList)

    def findDocs(self, fDic, find_all=True):
        # 查找数据库信息，可以传递一个bool类型find_all参数
        result = []
        if find_all:
            #在所有集合进行搜索,结果返回一个列表
            list = self.db.collection_names()
            #list.reverse()
            for coll in list:
                for x in self.db[coll].find(fDic):
                    result.append(x)
            # pprint(result)
            return result
        else:
            # 在指定集合进行搜索,手动输入集合或默认为当天，结果返回一个列表
            time = input("请输入查询日期（默认为当天<{}>）:".format(datetime.now().strftime("%Y%m%d"))) or datetime.now().strftime("%Y%m%d")
            #time_date = datetime(int(time[0:4]), int(time[4:6]), int(time[6:])).strftime("%Y-%m-%d")
            time_date = time[0:4] + "-" + time[4:6] + "-" + time[6:]
            find_col = self.db[time_date]
            for x in find_col.find(fDic):
                result.append(x)
            # pprint(result)
            return result




# class mongoWrite():
#     #mongo写入类
#     def __init__(self,iDictList):
#         #初始化数据库参数，连接数据库
#         self.client = MongoClient('219.216.87.8',27017)
#         self.db = self.client["aqi_record"]
#         #使用当前日期作为集合格式为（2017-10-20）
#         self.col = self.db[datetime.now().strftime("%Y-%m-%d")]
#         #写入数据库前将信息列表也作为属性初始化
#         self.iDictList = iDictList
#
#     def writeData(self):
#         #信息列表写入
#         new_post_list = self.iDictList
#         self.col.insert_many(new_post_list)
#
# class mongoFind():
#     # mongo搜索数据类
#     def __init__(self, iDict, time):
#         #需要传入待搜索的字典和搜索日期
#         self.client = MongoClient('219.216.87.8', 27017)
#         self.db = self.client["aqi_record"]
#         #如果time为空默认为当天，或者在输入的时间集合中搜索
#         if time == None :
#             self.col = self.db[datetime.now().strftime("%Y-%m-%d")]
#         else:
#             time_date = datetime(int(time[0:4]),int(time[4:6]),int(time[6:])).strftime("%Y-%m-%d")
#             self.col = self.db[time_date]
#         self.city_dic = iDict
#
#     def findDoc(self):
#     #在指定集合中搜索，返回一个列表
#         result = []
#         for x in self.col.find(self.city_dic):
#             result.append(x)
#         return result


class cityInfo():
    #定义城市信息类，主要属性是信息字典
    def __init__(self, name):
        self.iDict = {}
        self.url = "http://www.pm25.com/city/"
        self.city = name
        self.html = ""

    def getHTMLText(self):
        # 获取HTML页面
        url = self.url + self.city + '.html'
        try:
            r = requests.get(url)
            r.raise_for_status()
            r.encoding = "utf-8"
            return r.text
        except:
            return ""

    def getCityInfo(self):
        # 通过BeautifulSoup解析HTML，获取相关信息
        soup = BeautifulSoup(self.getHTMLText(), "html.parser")
        try:
            city = soup.find('span', attrs={"class": "city_name"}).string
            self.iDict["城市"] = city
            updateTime = soup.find('div', attrs={"class": "citydata_updatetime"}).string
            self.iDict["更新时间"] = updateTime[5:]  # 网页中的更新时间的内容为“更新时间：2017-09-30 14:00”，字典储存时只要后面的时间部分
            aqi = soup.find('a', attrs={"class": "cbol_aqi_num"}).string
            self.iDict["AQI指数"] = aqi
            return self.iDict
        except:
            self.iDict = {}

    # def getCityInfoUpdateTime(self):
    #     #建立更新时间查询方法
    #     update_time = self.iDict.get("更新时间")
    #     update_time_dic = {"更新时间":update_time}
    #     return update_time_dic


# def main():
## mongoWrite类测试用
#     dict1 = {"name":"test1", "value":"lalala"}
#     dict2 = {"name":"test2", "value":"hahaha"}
#     dict_list = [dict1, dict2]
#     mongoWrite(dict_list).writeData()

####################################
## cityInfo类测试用
#     shenyang = cityInfo("shenyang")
#     shenyang_html = shenyang.getHTMLText()
#     shenyang_iDict = cityInfo("shenyang").getCityInfo()
#     print(shenyang_iDict)
#
####################################
# mongoType类findDocs方法测试用
#     dic = {"城市":"沈阳"}
#     mongoType().findDocs(dic)
#     mongoType().findDocs(dic, find_all=False)
#
# if __name__ == '__main__':
#     main()

