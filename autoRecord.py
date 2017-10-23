#autoRecord.py

from classDef import mongoType, cityInfo
from datetime import datetime, timedelta
from pprint import pprint


def getInfoList(cityList):
    #从cityInfo类获取城市信息
    city_dict_list = []
    for city in cityList:
        city_dic = {}
        city_dic = cityInfo(city).getCityInfo()
        city_dict_list.append(city_dic)
    return city_dict_list

def mongoWrite(cityInfoList):
    #对城市字典列表进行写入，并对更新时间键值对进行全集合搜索
    f_dictt = cityInfoList[0]
    f_time = f_dictt["更新时间"]
    f_dict = {"更新时间":f_time}
    result = mongoType().findDocs(f_dict)
    #如果搜索到了内容则不进行数据库的写入
    if result != []:
        pprint(result)
        pprint("数据已存在，未写入数据库")
    # 如果没有搜索到了内容则进行数据库的写入
    else:
        mongoType().dicListWrite(cityInfoList)
        pprint(result)
        pprint("数据已写入数据库")


def main():
    #设定城市列表，四个城市
    city_list = ["shenyang", "haerbin", "changchun",  "beijing"]
    #设定时间循环
    delta = timedelta(seconds=20)
    now = datetime.now()
    begin = now
    end = now + timedelta(minutes=2)
    while now <= end:
        city_info_list = getInfoList(city_list)
        print("城市AQI结果：")
        pprint(city_info_list)
        mongoWrite(city_info_list)
        now += delta
    print("时间结束")


if __name__ == '__main__':
    main()
