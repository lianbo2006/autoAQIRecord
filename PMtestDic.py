#PMtestDic.py
#获取输入城市的空气AQI指数，并进行简单判断给出出行建议
import requests
from bs4 import BeautifulSoup
import re
import time
from pypinyin import lazy_pinyin


def getCityPinYin(city_str):
    # 将文字城市名转换为拼音
    city_pinyin = ''
    try:
        match = re.match(r"^[a-zA-z]+$", city_str)  # 使用正则匹配判断city_str是否为纯字母构成
        if match:
            city_pinyin = city_str.lower()  # 将city_pinyin全部降为小写，便于合成url
            return city_pinyin
        else:
            city_pinyin_list = lazy_pinyin(city_str)
            city_pinyin = ''.join(city_pinyin_list)  # 使用字符串的join()方法来进行城市列表拼音的拼接代替原有的循环方法
            return city_pinyin
    except:
        return ""

def getHTMLText(url,city):
    # 获取HTML页面
    url = url + city + '.html'
    try:
        r = requests.get(url)
        r.raise_for_status()
        r.encoding = "utf-8"
        return r.text
    except:
        return ""

def getCityInfo(html, iDict):
    # 通过BeautifulSoup解析HTML，获取相关信息
    soup = BeautifulSoup(html, "html.parser")
    try:
        city = soup.find('span', attrs={"class": "city_name"}).string
        iDict["城市"] = city
        updateTime = soup.find('div', attrs={"class": "citydata_updatetime"}).string
        iDict["更新时间"] = updateTime[5:] # 网页中的更新时间的内容为“更新时间：2017-09-30 14:00”，字典储存时只要后面的时间部分
        aqi =  soup.find('a', attrs={"class": "cbol_aqi_num"}).string
        iDict["AQI指数"] = aqi
        return iDict
    except:
        return ""

def printInfo(iDict):
    # 对信息字典进行输出
    if iDict == {}:
        print("程序运行错误，请重试")
    else:
        try:
            #循环打印键值对
            for key in iDict:
                print("{}:{}".format(key, iDict.get(key)))
            # 对aqi进行简单判断
            aqi_num = int(iDict.get("AQI指数"))
            if aqi_num <= 35:
                print("空气情况优秀，适合户外活动")
            elif aqi_num <= 75:
                print("空气情况良好，可以户外活动")
            else:
                print("空气情况一般，减少户外活动")
        except:
            return ""

def main():
    url = "http://www.pm25.com/city/"
    #city = '沈阳' # 调试用参数，此行可删除
    city = input("请输入需要查询的城市（沈阳/shenyang):")
    while city:
        time_start = time.clock()
        city_infoDict = {}
        city_pinyin = getCityPinYin(city)
        html = getHTMLText(url, city_pinyin)
        city_infoDict = getCityInfo(html, city_infoDict)
        printInfo(city_infoDict)
        time_end = time.clock()
        print("程序运行时间是 %-5.5ss" % (time_end - time_start))
        city = input("请输入需要查询的城市（沈阳/shenyang）:")

if __name__ == '__main__':
    main()
