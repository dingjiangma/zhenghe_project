from receive_mqtt import mqtt_rec
import json
import datetime
import time
import flask
from flask import Flask, Response,request
from flask import render_template
from mysql import Mysql
import threading
class DateEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj,datetime.datetime):
            return obj.strftime("%Y-%m-%d %H:%M:%S")
        else:
            return json.JSONEncoder.default(self,obj)
app = Flask(__name__)
app.jinja_env.variable_start_string = '(('  # 修改变量开始符号
app.jinja_env.variable_end_string = '))'  # 修改变量结束符号
@app.route("/")
def index():

    return render_template('search.html')
@app.route("/result", methods=['GET', 'POST'])
def index2():
    db = Mysql()
    if request.method == 'POST':
        startdate=request.form.get("startdate")
        start_list=startdate.split("T")
        starttime=start_list[0]+' '+start_list[1]+':00'
        enddate = request.form.get("enddate")
        end_list = enddate.split("T")
        endtime = end_list[0] + ' ' + end_list[1] + ':00'
        addr=str(request.form.get("addr"))
    mess=[]
    mess=[addr,starttime,endtime]
    print(mess)
    items = db.getItems(mess)
    iit = list(items)
    value = []
    for i in range(0, len(iit)):
        value.append(items[i][0])
    print(value)
    time = []
    for i in range(0, len(iit)):
        time.append(items[i][1])
    print(time)
    time_change = []
    for tim in time:
        time_change.append(tim.strftime("%Y-%m-%d %H:%M:%S"))
    print(time_change)
    return render_template('result.html',value=value,time=time_change)
def web():
    app.run(debug=True,use_reloader=False)
def mqtt():
    mqtt_rec().recive('zwl', 0, 'broker-cn.emqx.io', 1883, 'zwl', '123456')
if __name__ == '__main__':
    sing_thread = threading.Thread(target=web)
    song_thread = threading.Thread(target=mqtt)
    sing_thread.start()
    song_thread.start()
    	#debug=True发生错误时会返回发生错误的地方