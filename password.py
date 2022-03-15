import pymysql
from werkzeug.security import generate_password_hash, check_password_hash


class pwd(object):
    def __init__(self):
        try:
            self.conn = pymysql.connect(host='localhost', user='root', password='123456', database='int30',
                                        charset="utf8")
            self.cursor = self.conn.cursor()  # 用来获得python执行Mysql命令的方法（游标操作）
            print("连接数据库成功")
        except Exception:
            print("连接失败")

    def password_register(self, name, pwd_origin, email):
        pwd_hash = generate_password_hash(pwd_origin)
        char_all = [name, pwd_hash, email]
        try:
            sql = """INSERT INTO pwd(
                name,
                pwd,
                email)
                VALUES (%s,%s,%s)
                """
            self.cursor.execute(sql, char_all)
            # self.cursor.commit()
            print("密码存储成功")
        except Exception:
            # self.cursor.rollback()
            print("未保存成功，请再尝试")

    def password_check(self, namee, pwd_insert):
        sql = """SELECT pwd from pwd where name = %s """
        self.cursor.execute(sql,pymysql.converters.escape_string(namee))
        pwd_hash = self.cursor.fetchone()
        print(pwd_hash[0])
        result = check_password_hash(pwd_hash[0], pwd_insert)
        if result:
            print("密码正确")
        return result

    def password_notsame(self, name):
        sql = """SELECT name from pwd
            """
        self.cursor.execute(sql)
        name_all = self.cursor.fetchall()
        for i in range(0, len(name_all)):
            if name_all[i][0] == name:
                print("存在重名")
                return False
        return True
