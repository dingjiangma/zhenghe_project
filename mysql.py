import pymysql
from datetime import datetime
import time


class Mysql(object):
    def __init__(self):
        try:
            self.conn = pymysql.connect(host='localhost', user='root', password='123456', database='int30',
                                        charset="utf8")
            self.cursor = self.conn.cursor()  # 用来获得python执行Mysql命令的方法（游标操作）
            print("连接数据库成功")
        except:
            print("连接失败")

    def getItems(self, data):
        sql = "select value,time_update from meter where addr=%s and time_update>=%s and time_update<=%s order by time_update asc"  # 获取food数据表的内容
        self.cursor.execute(sql, data)
        items = self.cursor.fetchall()  # 接收全部的返回结果行
        return items


if __name__ == '__main__':
    hihi = Mysql()
    items = hihi.getItems(['42', '2022-03-04 16:15:00', '2022-03-04 16:16:00'])
    print(items)
    iit = list(items)
    print(len(iit))
    value = []
    for i in range(0, len(iit)):
        value.append(items[i][0])
    print(value)
    time = []
    for i in range(0, len(iit)):
        time.append(items[i][1])
    print(time[2])
    timee = time[2].timetuple()
    time_change = []
    for tim in time:
        time_change.append(tim.strftime("%Y-%m-%d %H:%M:%S"))
    print(time_change)
    # 时间字符串化
