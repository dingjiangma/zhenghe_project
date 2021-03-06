from receive_mqtt import mqtt_rec
import json
import datetime
import time
import flask
from flask import Flask, Response, request, session, redirect, url_for, make_response
from flask import render_template
from mysql import Mysql
import threading
from numpy import *
from password import pwd


class DateEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime("%Y-%m-%d %H:%M:%S")
        else:
            return json.JSONEncoder.default(self, obj)


app = Flask(__name__)
app.jinja_env.variable_start_string = '(('  # 修改变量开始符号
app.jinja_env.variable_end_string = '))'  # 修改变量结束符号
app.secret_key = 'fkdjsafjdklkjfadskjfadskljdsfklj'


@app.route("/")
def index():
    return render_template('index_reg.html')


@app.route("/denglu", methods=['GET', 'POST'])
def indexx():
    pd = pwd()
    if request.method == 'POST':
        print("收到了消息")
        print(request.form.get("name"))
        print(request.form.get("password"))
        namee = str(request.form.get("name"))
        pwd_insert = str(request.form.get("password"))
        if pd.password_check(namee, pwd_insert):
            session['username'] = request.form.get("name")
            print('可以登录')
            return redirect(url_for('index4'))
    return redirect(url_for('index'))


@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    pd = pwd()
    if request.method == 'POST':
        print(request.form.get("email"))
        if pd.password_notsame(request.form.get("name")):
            print("没有重复")
            pd.password_register(request.form.get("name"), request.form.get(
                "password"), request.form.get("email"))
            return redirect(url_for('index'))
        else:
            return render_template('register.html', mess='用户名已存在，换一个吧')
    return render_template('register.html', mess='注册')


@app.route("/result", methods=['GET', 'POST'])
def index2():
    if 'username' in session:
        db = Mysql()
        if request.method == 'POST':
            startdate = request.form.get("startdate")
            start_list = startdate.split("T")
            starttime = start_list[0] + ' ' + start_list[1] + ':00'
            enddate = request.form.get("enddate")
            end_list = enddate.split("T")
            endtime = end_list[0] + ' ' + end_list[1] + ':00'
            addr = str(request.form.get("addr"))
        mess = []
        mess = [addr, starttime, endtime]
        print(mess)
        items = db.getItems(mess)
        iit = list(items)
        value = []
        for i in range(0, len(iit)):
            value.append(items[i][0])
        # print(value)
        time = []
        for i in range(0, len(iit)):
            time.append(items[i][1])
        # print(time)
        time_change = []
        for tim in time:
            time_change.append(tim.strftime("%Y-%m-%d %H:%M:%S"))
        # print(time_change)
        return render_template('result.html', value=value, time=time_change)
    else:
        return redirect(url_for('index'))


@app.route("/charts")
def index3():
    if 'username' in session:
        db = Mysql()
        pa1 = [26, '2022-03-11 15:45:00', '2022-03-30 15:45:00']
        pa2 = [38, '2022-03-11 15:45:00', '2022-03-30 15:45:00']
        qa1 = [30, '2022-03-11 15:45:00', '2022-03-30 15:45:00']
        qa2 = [42, '2022-03-11 15:45:00', '2022-03-30 15:45:00']
        pa1_value = db.trans_value(db.getItems(pa1))
        pa1_adv = mean(pa1_value)
        pa2_value = db.trans_value(db.getItems(pa2))
        pa2_adv = mean(pa2_value)
        qa1_value = db.trans_value(db.getItems(qa1))
        qa1_adv = mean(qa1_value)
        qa2_value = db.trans_value(db.getItems(qa2))
        qa2_adv = mean(qa2_value)
        lenth = len(qa2_value)
        time = db.trans_time(db.getItems(qa1))
        ia1 = [16, '2022-03-11 15:45:00', '2022-03-30 15:45:00']
        ia2 = [21, '2022-03-11 15:45:00', '2022-03-30 15:45:00']
        ia1_value = db.trans_value(db.getItems(ia1))
        ia1_value = ia1_value[-41:-1]
        ia2_value = db.trans_value(db.getItems(ia2))
        ia2_value = ia2_value[-41:-1]
        time_20 = time[-41:-1]

        print(ia2_value)
        return render_template('chart.html', pa1_adv=pa1_adv, pa2_adv=pa2_adv, qa1_adv=qa1_adv, qa2_adv=qa2_adv, time=time_20, ia1=ia1_value, ia2=ia2_value, time_all=time, pa2=pa2_value, qa2=qa2_value, pa1=pa1_value, qa1=qa1_value)
    else:
        return redirect(url_for('index'))


@app.route("/main")
def index4():
    if 'username' in session:
        print(session['username'])
        db = Mysql()
        pa1 = [26, '2022-03-11 15:45:00', '2022-03-30 15:45:00']
        pa2 = [38, '2022-03-11 15:45:00', '2022-03-30 15:45:00']
        qa1 = [30, '2022-03-11 15:45:00', '2022-03-30 15:45:00']
        qa2 = [42, '2022-03-11 15:45:00', '2022-03-30 15:45:00']
        pa1_value = db.trans_value(db.getItems(pa1))
        pa1_adv = mean(pa1_value)
        pa2_value = db.trans_value(db.getItems(pa2))
        pa2_adv = mean(pa2_value)
        qa1_value = db.trans_value(db.getItems(qa1))
        qa1_adv = mean(qa1_value)
        qa2_value = db.trans_value(db.getItems(qa2))
        qa2_adv = mean(qa2_value)
        lenth = len(qa2_value)
        time = db.trans_time(db.getItems(qa1))
        ia1 = [16, '2022-03-11 15:45:00', '2022-03-30 15:45:00']
        ia2 = [21, '2022-03-11 15:45:00', '2022-03-30 15:45:00']
        ia1_value = db.trans_value(db.getItems(ia1))
        pa1_value_20 = pa1_value[-10:-1]
        ia2_value = db.trans_value(db.getItems(ia2))
        pa2_value_20 = pa2_value[-10:-1]
        time_20 = time[-10:-1]
        return render_template('index.html', pa1_adv=pa1_adv, pa2_adv=pa2_adv, qa1_adv=qa1_adv, qa2_adv=qa2_adv, time_20=time_20, pa1_20=pa1_value_20, pa2_20=pa2_value_20)
    else:
        return redirect(url_for('index'))


@app.route("/search")
def index_search():
    if 'username' in session:
        return render_template('ui-elements.html')
    else:
        return redirect(url_for('index'))


def web():
    app.run(debug=True, use_reloader=False)
# debug=True发生错误时会返回发生错误的地方


def mqtt():
    mqtt_rec().recive('zwl', 0, 'broker-cn.emqx.io', 1883, 'zwl', '123456')


if __name__ == '__main__':
    sing_thread = threading.Thread(target=web)
    # song_thread = threading.Thread(target=mqtt)
    # 双线程工作
    sing_thread.start()
    # song_thread.start()
