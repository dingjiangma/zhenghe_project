import pymysql


class trans(object):
    def __init__(self):
        try:
            self.conn = pymysql.connect(host='localhost', user='root', password='123456', database='int30',
                                        charset="utf8")
            self.cursor = self.conn.cursor()  # 用来获得python执行Mysql命令的方法（游标操作）
            print("连接数据库成功")
        except:
            print("连接失败")

    def tran(self, mess):
        mess_change = mess.split()
        address = int(mess_change[1])
        sql = """select unit,name,remark from danwei where addr = %s"""
        self.cursor.execute(sql, address)
        items = self.cursor.fetchall()
        back = mess_change + list(items[0])
        print(back)
        return (back)


if __name__ == '__main__':
    app = '0 38 12.5'
    print(app)
    wahah = trans()
    akk = wahah.tran(app)
