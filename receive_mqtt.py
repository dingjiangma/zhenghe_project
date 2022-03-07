import paho.mqtt.client as mqtt
from paho.mqtt.client import Client
import pymysql
data =''

def on_connect(client, userdata, flags, rc):
    print("Connected with result code: " + str(rc))



def on_message(client, userdata, msg):
    print(msg.topic + "的内容是" + msg.payload.decode())
    global data
    data=msg.payload.decode()
    try:
        db = pymysql.connect(host='localhost', user='root', password='123456', database='int30')
        cursor = db.cursor()
        print("数据库连接 成功")
    except:
        print("数据库连接失败")
    chang=data.spilt()
    change=[]
    change.append(int(chang[0]))
    change.append(int(chang[1]))
    change.append(float(chang[2]))
    change.append(chang[3])
    change.append(chang[4])
    change.append(chang[5])
    try:
        sql = """INSERT INTO meter(
       ID,
       addr,
       value,
       unit,
       name,
       remark
       )
       VALUES (%s,%s,%s,%s,%s,%s)
       """
        cursor.execute(sql, change)
        db.commit()
        print("数据库数据已更新")
    except:
        # 发生错误时回滚
        db.rollback()
        print("数据库未修改，请再尝试")
    print(data)
class mqtt_rec(object):
    def recive(self,theme,qos,net,port,name,password):
        client: Client = mqtt.Client()
        client.on_connect = on_connect
        client.on_message = on_message
        client.connect(net, port, 600) # 600为keepalive的时间间隔
        client.username_pw_set(name, password)
        client.subscribe(theme, qos=qos)
        client.loop_forever() # 保持连接
if __name__ == '__main__':
    mqtt_rec().recive('zwl',0,'127.0.0.1',1883,'zwl','123456')
    print(data)